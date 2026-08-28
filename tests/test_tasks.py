"""tests/test_tasks.py — TC: CRUD Task + Day-H reminder sync + filter + state machine."""
from datetime import datetime, timedelta

import pytest

from app.extensions import db
from app.models import Reminder, ReminderType, Task
from app.services.project_service import project_service
from app.services.task_service import task_service


@pytest.fixture
def sample_project(app):
    return project_service.create(name="Pekerjaan", color="#3B82F6", icon="briefcase")


@pytest.fixture
def sample_task(app, sample_project):
    return task_service.create(
        title="Finalisasi laporan",
        project_id=sample_project.id,
        priority="high",
        deadline=datetime.now() + timedelta(days=3),
    )


def _day_h_count(task_id: int) -> int:
    return (
        db.session.query(Reminder)
        .filter_by(task_id=task_id, reminder_type=ReminderType.DAY_H)
        .count()
    )


class TestTaskService:
    """TC-07: CRUD Task via service."""

    def test_create_berhasil_default(self, app):
        task = task_service.create(title="Tugas baru")
        assert task.id is not None
        assert task.priority.value == "medium"
        assert task.status.value == "todo"
        assert task.completed_at is None

    def test_create_judul_kosong_valueerror(self, app):
        with pytest.raises(ValueError, match="wajib diisi"):
            task_service.create(title="  ")

    def test_create_project_tidak_ada_valueerror(self, app):
        with pytest.raises(ValueError, match="Project tidak ditemukan"):
            task_service.create(title="X", project_id=999)

    def test_toggle_complete_jaga_completed_at(self, sample_task):
        sample_task  # noqa: B018 — fixture trigger
        done = task_service.toggle_complete(sample_task.id)
        assert done.status.value == "done"
        assert done.completed_at is not None
        reopened = task_service.toggle_complete(sample_task.id)
        assert reopened.status.value == "todo"
        assert reopened.completed_at is None

    def test_update_status_done_set_completed_at(self, sample_task):
        task_service.update(
            sample_task.id,
            title=sample_task.title,
            project_id=sample_task.project_id,
            priority="high",
            status="done",
            deadline=sample_task.deadline,
        )
        assert sample_task.completed_at is not None


class TestUpdateStatusService:
    """TC-11a: update_status (kanban) — state machine tanpa ubah field lain."""

    def test_todo_ke_done_set_completed_at(self, sample_task):
        task = task_service.update_status(sample_task.id, "done")
        assert task.status.value == "done"
        assert task.completed_at is not None

    def test_done_ke_proses_hapus_completed_at(self, sample_task):
        task_service.update_status(sample_task.id, "done")
        task = task_service.update_status(sample_task.id, "in_progress")
        assert task.status.value == "in_progress"
        assert task.completed_at is None

    def test_todo_ke_proses_tidak_set_completed_at(self, sample_task):
        task = task_service.update_status(sample_task.id, "in_progress")
        assert task.status.value == "in_progress"
        assert task.completed_at is None

    def test_status_invalid_valueerror(self, sample_task):
        with pytest.raises(ValueError, match="Status harus"):
            task_service.update_status(sample_task.id, "batal")

    def test_task_tidak_ada_valueerror(self, app):
        with pytest.raises(ValueError, match="Tugas tidak ditemukan"):
            task_service.update_status(999, "done")


class TestDayHReminderSync:
    """TC-08: Reminder Day-H otomatis mengikuti deadline."""

    def test_deadline_dibuat_reminder_hadir(self, sample_task):
        assert _day_h_count(sample_task.id) == 1

    def test_tanpa_deadline_tanpa_reminder(self, app):
        task = task_service.create(title="Tanpa deadline")
        assert _day_h_count(task.id) == 0

    def test_deadline_dihapus_reminder_terhapus(self, sample_task):
        task_service.update(
            sample_task.id,
            title=sample_task.title,
            project_id=sample_task.project_id,
            priority="high",
            status="todo",
            deadline=None,
        )
        assert _day_h_count(sample_task.id) == 0

    def test_deadline_diubah_reminder_tetap_satu(self, sample_task):
        task_service.update(
            sample_task.id,
            title=sample_task.title,
            project_id=sample_task.project_id,
            priority="high",
            status="todo",
            deadline=datetime.now() + timedelta(days=10),
        )
        assert _day_h_count(sample_task.id) == 1


class TestTaskFilters:
    """TC-09: Filter & sort daftar task."""

    def test_filter_status_dan_priority(self, app, sample_project):
        task_service.create(title="A", priority="high", status="done")
        task_service.create(title="B", priority="low", status="in_progress")
        task_service.create(title="C", priority="high")

        done = task_service.get_all(filters={"status": "done"})
        assert [t.title for t in done] == ["A"]

        high = task_service.get_all(filters={"priority": "high", "status": "todo"})
        assert [t.title for t in high] == ["C"]

    def test_filter_project_dan_done_diturunkan(self, app, sample_project):
        task_service.create(title="Dalam project", project_id=sample_project.id)
        task_service.create(title="Inbox")
        task_service.create(title="Selesai", status="done", project_id=sample_project.id)

        views = task_service.get_all(filters={"project_id": sample_project.id})
        assert views[0].title == "Dalam project"  # done paling bawah
        assert views[-1].title == "Selesai"


class TestTaskRoutes:
    """TC-10: Task routes (PRG + proteksi)."""

    def test_create_via_post_persist(self, client, login_user, sample_project):
        response = client.post(
            "/tasks/create",
            data={
                "title": "Tugas dari browser",
                "description": "Deskripsi",
                "project_id": str(sample_project.id),
                "priority": "high",
                "status": "todo",
                "deadline": "2026-09-05T14:30",
            },
            follow_redirects=False,
        )
        assert response.status_code == 302
        task = db.session.query(Task).filter_by(title="Tugas dari browser").first()
        assert task is not None
        assert task.priority.value == "high"
        assert task.deadline == datetime(2026, 9, 5, 14, 30)
        assert _day_h_count(task.id) == 1

    def test_detail_404_bila_tidak_ada(self, client, login_user):
        assert client.get("/tasks/999").status_code == 404

    def test_complete_via_post_toggle(self, client, login_user, sample_task):
        client.post(f"/tasks/{sample_task.id}/complete")
        assert db.session.get(Task, sample_task.id).status.value == "done"
        client.post(f"/tasks/{sample_task.id}/complete")
        assert db.session.get(Task, sample_task.id).status.value == "todo"

    def test_complete_tanpa_xhr_tetap_redirect_prg(self, client, login_user, sample_task):
        response = client.post(f"/tasks/{sample_task.id}/complete", follow_redirects=False)
        assert response.status_code == 302

    def test_complete_xhr_balas_json(self, client, login_user, sample_task):
        headers = {"X-Requested-With": "fetch"}
        done = client.post(f"/tasks/{sample_task.id}/complete", headers=headers)
        assert done.status_code == 200
        payload = done.get_json()
        assert payload["status"] == "ok"
        assert payload["data"]["status"] == "done"
        reopened = client.post(f"/tasks/{sample_task.id}/complete", headers=headers)
        assert reopened.get_json()["data"]["status"] == "todo"

    def test_complete_xhr_404_json(self, client, login_user):
        response = client.post("/tasks/999/complete", headers={"X-Requested-With": "fetch"})
        assert response.status_code == 404
        assert response.get_json()["status"] == "error"

    def test_delete_via_post_hapus_row(self, client, login_user, sample_task):
        task_id = sample_task.id
        client.post(f"/tasks/{task_id}/delete")
        assert db.session.get(Task, task_id) is None

    def test_edit_prefill_render(self, client, login_user, sample_task):
        response = client.get(f"/tasks/{sample_task.id}/edit")
        assert response.status_code == 200
        body = response.data.decode()
        assert "Finalisasi laporan" in body
        assert 'value="high"' in body  # priority ter-select


class TestKanbanRoutes:
    """TC-11b: Board kanban + endpoint ubah status (drag & drop)."""

    def test_kanban_render_3_kolom(self, client, login_user, sample_task):
        response = client.get("/tasks/kanban")
        assert response.status_code == 200
        body = response.data.decode()
        assert 'data-kanban-column="todo"' in body
        assert 'data-kanban-column="in_progress"' in body
        assert 'data-kanban-column="done"' in body
        assert "Finalisasi laporan" in body

    def test_kanban_grouping_per_status(self, client, login_user, sample_project):
        todo = task_service.create(title="Belum", project_id=sample_project.id)
        proses = task_service.create(title="Jalan", project_id=sample_project.id)
        task_service.update_status(proses.id, "in_progress")

        body = client.get("/tasks/kanban").data.decode()
        pos_todo_card = body.find(f'data-task-id="{todo.id}"')
        pos_todo_col = body.find('data-kanban-column="todo"')
        pos_proses_col = body.find('data-kanban-column="in_progress"')
        assert pos_todo_col < pos_todo_card < pos_proses_col

    def test_status_post_xhr_json(self, client, login_user, sample_task):
        headers = {"X-Requested-With": "fetch", "Content-Type": "application/json"}
        response = client.post(
            f"/tasks/{sample_task.id}/status", headers=headers, json={"status": "done"}
        )
        assert response.status_code == 200
        payload = response.get_json()
        assert payload["status"] == "ok"
        assert payload["data"]["status"] == "done"
        assert db.session.get(Task, sample_task.id).status.value == "done"

    def test_status_post_invalid_400_json(self, client, login_user, sample_task):
        headers = {"X-Requested-With": "fetch", "Content-Type": "application/json"}
        response = client.post(
            f"/tasks/{sample_task.id}/status", headers=headers, json={"status": "batal"}
        )
        assert response.status_code == 400
        assert response.get_json()["status"] == "error"
        assert db.session.get(Task, sample_task.id).status.value == "todo"

    def test_status_post_404_json(self, client, login_user):
        headers = {"X-Requested-With": "fetch", "Content-Type": "application/json"}
        response = client.post("/tasks/999/status", headers=headers, json={"status": "done"})
        assert response.status_code == 404
        assert response.get_json()["status"] == "error"

    def test_status_post_tanpa_xhr_redirect_prg(self, client, login_user, sample_task):
        response = client.post(
            f"/tasks/{sample_task.id}/status",
            content_type="application/json",
            data='{"status": "done"}',
            follow_redirects=False,
        )
        assert response.status_code == 302
        assert "/tasks/kanban" in response.headers["Location"]

    def test_kanban_tanpa_login_redirect(self, client):
        assert client.get("/tasks/kanban").status_code == 302
