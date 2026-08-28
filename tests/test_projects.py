"""tests/test_projects.py — TC: CRUD Project (service + route)."""
import pytest

from app.extensions import db
from app.models import Project, Task
from app.services.project_service import project_service
from app.services.task_service import task_service


@pytest.fixture
def sample_project(app):
    return project_service.create(name="Pekerjaan", color="#3B82F6", icon="briefcase")


class TestProjectService:
    """TC-04: CRUD Project via service."""

    def test_create_berhasil(self, sample_project):
        assert sample_project.id is not None
        assert sample_project.name == "Pekerjaan"
        assert sample_project.color == "#3B82F6"

    def test_create_nama_kosong_valueerror(self, app):
        with pytest.raises(ValueError, match="wajib diisi"):
            project_service.create(name="   ", color="#3B82F6")

    def test_create_warna_invalid_valueerror(self, app):
        with pytest.raises(ValueError, match="hex"):
            project_service.create(name="X", color="merah")

    def test_update_berhasil(self, sample_project):
        updated = project_service.update(sample_project.id, name="Kantor", color="#8B5CF6", icon="building")
        assert updated.name == "Kantor"
        assert updated.color == "#8B5CF6"

    def test_update_tidak_ada_valueerror(self, app):
        with pytest.raises(ValueError, match="tidak ditemukan"):
            project_service.update(999, name="X", color="#3B82F6")

    def test_archive_dan_pulihkan(self, sample_project):
        assert project_service.set_archived(sample_project.id, True).archived is True
        assert project_service.get_all() == []  # exclude archived by default
        assert project_service.set_archived(sample_project.id, False).archived is False

    def test_delete_melepas_task_bukan_menghapus(self, sample_project):
        task = task_service.create(title="Tugas A", project_id=sample_project.id)
        project_service.delete(sample_project.id)
        db.session.expire_all()
        surviving = db.session.get(Task, task.id)
        assert surviving is not None
        assert surviving.project_id is None


class TestProjectCounts:
    """TC-05: Counts aggregate untuk kartu project."""

    def test_counts_dihitung_benar(self, sample_project):
        task_service.create(title="T1", project_id=sample_project.id, status="done")
        task_service.create(title="T2", project_id=sample_project.id)
        view = project_service.get_by_id(sample_project.id)
        assert view is not None
        assert view.total_tasks == 2
        assert view.done_tasks == 1
        assert view.active_tasks == 1

    def test_count_all_project(self, sample_project):
        other = project_service.create(name="Arsip", color="#111111")
        project_service.set_archived(other.id, True)
        total, active = project_service.count_all()
        assert total == 2
        assert active == 1


class TestProjectRoutes:
    """TC-06: Project routes (PRG + proteksi)."""

    def test_list_tampil(self, client, login_user, sample_project):
        response = client.get("/projects/")
        assert response.status_code == 200
        assert b"Pekerjaan" in response.data

    def test_detail_404_bila_tidak_ada(self, client, login_user):
        assert client.get("/projects/999").status_code == 404

    def test_create_via_post_persist_dan_redirect(self, client, login_user):
        response = client.post(
            "/projects/create",
            data={"name": "Rumah", "color": "#10B981", "icon": "house"},
            follow_redirects=False,
        )
        assert response.status_code == 302
        assert db.session.query(Project).filter_by(name="Rumah").first() is not None

    def test_create_invalid_flash_error_dan_tanpa_persist(self, client, login_user):
        response = client.post(
            "/projects/create",
            data={"name": "X", "color": "bukan-hex", "icon": ""},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"hex" in response.data
        assert db.session.query(Project).filter_by(name="X").first() is None
