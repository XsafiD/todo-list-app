"""tests/test_archive.py — TC: arsip task (service + routes + invariant state machine)."""
import pytest

from app.extensions import db
from app.models import Task
from app.services.project_service import project_service
from app.services.task_service import task_service


@pytest.fixture
def sample_project(app):
    return project_service.create(name="Pekerjaan", color="#3B82F6", icon="briefcase")


@pytest.fixture
def done_task(app, sample_project):
    task = task_service.create(title="Tugas selesai", project_id=sample_project.id)
    return task_service.update_status(task.id, "done")


@pytest.fixture
def archived_task(app, done_task):
    return task_service.archive(done_task.id)


class TestArchiveService:
    """TC-12a: arsip/unarchive via service — delegasi state machine."""

    def test_archive_dari_todo_valueerror(self, app):
        task = task_service.create(title="Belum selesai")
        with pytest.raises(ValueError, match="tidak dapat diarsipkan"):
            task_service.archive(task.id)

    def test_archive_dari_done_set_archived_at(self, done_task):
        task = task_service.archive(done_task.id)
        assert task.status.value == "done"
        assert task.archived_at is not None
        assert task.completed_at is not None

    def test_archive_idempotent_tidak_reset_timestamp(self, archived_task):
        first = archived_task.archived_at
        task = task_service.archive(archived_task.id)
        assert task.archived_at == first

    def test_archive_task_tidak_ada_valueerror(self, app):
        with pytest.raises(ValueError, match="Tugas tidak ditemukan"):
            task_service.archive(999)

    def test_archived_hilang_dari_get_all_muncul_di_get_archived(self, archived_task):
        active = task_service.get_all()
        assert all(t.id != archived_task.id for t in active)

        archived = task_service.get_archived()
        assert [t.id for t in archived] == [archived_task.id]
        assert archived[0].archived_at is not None

    def test_get_archived_filter_project(self, app, sample_project, archived_task):
        task_service.create(title="Inbox selesai", status="done")
        inbox_done = task_service.get_all(filters={"status": "done"})[0]
        task_service.archive(inbox_done.id)

        views = task_service.get_archived(filters={"project_id": sample_project.id})
        assert [t.id for t in views] == [archived_task.id]

    def test_get_archived_sort_terbaru_dulu(self, app):
        for i in range(3):
            task = task_service.create(title=f"T{i}", status="done")
            task_service.archive(task.id)

        views = task_service.get_archived()
        assert views[0].archived_at >= views[-1].archived_at

    def test_unarchive_status_tetap_done(self, archived_task):
        task = task_service.unarchive(archived_task.id)
        assert task.archived_at is None
        assert task.status.value == "done"
        assert task.completed_at is not None
        assert any(t.id == task.id for t in task_service.get_all())

    def test_unarchive_task_tidak_ada_valueerror(self, app):
        with pytest.raises(ValueError, match="Tugas tidak ditemukan"):
            task_service.unarchive(999)


class TestArchiveInvariant:
    """TC-12b: invariant — task terarsip selalu done; meninggalkan done = keluar arsip."""

    def test_update_status_dari_archived_clear_archived_at(self, archived_task):
        task = task_service.update_status(archived_task.id, "in_progress")
        assert task.status.value == "in_progress"
        assert task.archived_at is None

    def test_toggle_complete_dari_archived_clear_archived_at(self, archived_task):
        task = task_service.toggle_complete(archived_task.id)
        assert task.status.value == "todo"
        assert task.archived_at is None

    def test_delete_task_terarsip(self, archived_task):
        task_id = archived_task.id
        task_service.delete(task_id)
        assert db.session.get(Task, task_id) is None


class TestArchiveRoutes:
    """TC-12c: routes arsip (PRG + proteksi + anti open redirect)."""

    def test_arsip_tanpa_login_redirect(self, client):
        assert client.get("/arsip/").status_code == 302

    def test_arsip_render_list(self, client, login_user, archived_task):
        response = client.get("/arsip/")
        assert response.status_code == 200
        body = response.data.decode()
        assert "Tugas selesai" in body
        assert 'data-modal-target="modal-delete-archived-task"' in body

    def test_arsip_kosong_empty_state(self, client, login_user):
        body = client.get("/arsip/").data.decode()
        assert "Belum ada arsip" in body

    def test_arsip_filter_project(self, client, login_user, sample_project, archived_task):
        body = client.get(f"/arsip/?project_id={sample_project.id + 999}").data.decode()
        assert "Tugas selesai" not in body
        assert "Tidak ada arsip" in body

    def test_archive_post_prg_dari_kanban(self, client, login_user, done_task):
        response = client.post(f"/tasks/{done_task.id}/archive", follow_redirects=False)
        assert response.status_code == 302
        assert "/tasks/kanban" in response.headers["Location"]
        assert db.session.get(Task, done_task.id).archived_at is not None

    def test_archive_post_task_aktif_flash_error(self, client, login_user):
        task = task_service.create(title="Masih jalan")
        response = client.post(f"/tasks/{task.id}/archive", follow_redirects=True)
        assert response.status_code == 200
        assert db.session.get(Task, task.id).archived_at is None

    def test_archive_post_404(self, client, login_user):
        assert client.post("/tasks/999/archive").status_code == 404

    def test_unarchive_post_prg_kembali_ke_arsip(self, client, login_user, archived_task):
        response = client.post(f"/tasks/{archived_task.id}/unarchive", follow_redirects=False)
        assert response.status_code == 302
        assert "/arsip/" in response.headers["Location"]
        row = db.session.get(Task, archived_task.id)
        assert row.archived_at is None
        assert row.status.value == "done"

    def test_unarchive_post_404(self, client, login_user):
        assert client.post("/tasks/999/unarchive").status_code == 404

    def test_delete_dari_arsip_next_kembali_ke_arsip(self, client, login_user, archived_task):
        task_id = archived_task.id
        response = client.post(
            f"/tasks/{task_id}/delete", data={"next": "/arsip/"}, follow_redirects=False
        )
        assert response.status_code == 302
        assert "/arsip/" in response.headers["Location"]
        assert db.session.get(Task, task_id) is None

    def test_delete_next_eksternal_ditolak_fallback(self, client, login_user, done_task):
        """Anti open redirect — next absolut tidak dipakai (16-security.md)."""
        task_id = done_task.id
        response = client.post(
            f"/tasks/{task_id}/delete",
            data={"next": "https://evil.example.com/"},
            follow_redirects=False,
        )
        assert response.status_code == 302
        assert response.headers["Location"].startswith("/")
        assert "evil.example.com" not in response.headers["Location"]

    def test_kanban_tidak_menampilkan_task_terarsip(self, client, login_user, archived_task):
        body = client.get("/tasks/kanban").data.decode()
        assert f'data-task-id="{archived_task.id}"' not in body

    def test_sidebar_dan_bottom_nav_memuat_menu_arsip(self, client, login_user):
        body = client.get("/arsip/").data.decode()
        assert 'href="/arsip/"' in body
