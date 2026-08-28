"""tests/test_setting.py — TC: setting service + scheduler job + routes Pengaturan."""
import pytest

from app.extensions import db
from app.models import Setting, Task
from app.scheduler import run_auto_archive
from app.services.setting_service import (
    AUTO_ARCHIVE_ENABLED,
    AUTO_ARCHIVE_LAST_RUN_AT,
    AUTO_ARCHIVE_LAST_RUN_COUNT,
    setting_service,
)
from app.services.task_service import task_service


@pytest.fixture
def done_tasks(app):
    """2 task done aktif + 1 todo + 1 done sudah terarsip."""
    done_a = task_service.create(title="Selesai A", status="done")
    done_b = task_service.create(title="Selesai B", status="done")
    todo = task_service.create(title="Belum")
    archived = task_service.create(title="Sudah arsip", status="done")
    task_service.archive(archived.id)
    return done_a, done_b, todo, archived


class TestSettingService:
    """TC-13a: CRUD konfigurasi key-value."""

    def test_get_default_none_dan_bool_false(self, app):
        assert setting_service.get("tidak_ada") is None
        assert setting_service.get_bool("tidak_ada") is False
        assert setting_service.get_bool("tidak_ada", default=True) is True

    def test_set_bool_dan_get_bool_roundtrip(self, app):
        setting_service.set(AUTO_ARCHIVE_ENABLED, True)
        assert setting_service.get_bool(AUTO_ARCHIVE_ENABLED) is True
        setting_service.set(AUTO_ARCHIVE_ENABLED, False)
        assert setting_service.get_bool(AUTO_ARCHIVE_ENABLED) is False

    def test_set_upsert_tidak_duplikat_row(self, app):
        setting_service.set("kunci", "satu")
        setting_service.set("kunci", "dua")
        rows = db.session.query(Setting).filter_by(name="kunci").all()
        assert len(rows) == 1
        assert rows[0].value == "dua"

    def test_get_int_nilai_salah_fallback_default(self, app):
        setting_service.set("angka", "bukan-angka")
        assert setting_service.get_int("angka", default=7) == 7

    def test_get_int_none_fallback_default(self, app):
        assert setting_service.get_int("tidak_ada", default=3) == 3


class TestArchiveAllCompleted:
    """TC-13b: batch arsip untuk job otomatis."""

    def test_arsip_semua_done_aktif_saja(self, done_tasks):
        done_a, done_b, todo, archived = done_tasks
        count = task_service.archive_all_completed()

        assert count == 2  # done aktif saja
        for task in (done_a, done_b, todo, archived):
            row = db.session.get(Task, task.id)
            expected_archived = task.id != todo.id
            assert (row.archived_at is not None) is expected_archived
            assert row.status.value == ("todo" if task is todo else "done")

    def test_idempotent_run_kedua_nol(self, done_tasks):
        task_service.archive_all_completed()
        assert task_service.archive_all_completed() == 0


class TestAutoArchiveJob:
    """TC-13c: job scheduler — baca toggle saat runtime."""

    def test_off_noop_tidak_arsip_dan_tidak_catat(self, app, done_tasks):
        run_auto_archive(app)  # default off
        assert task_service.get_all()  # masih ada task aktif (2 done + 1 todo)
        assert setting_service.get(AUTO_ARCHIVE_LAST_RUN_AT) is None

    def test_on_arsipkan_dan_catat_last_run(self, app, done_tasks):
        setting_service.set(AUTO_ARCHIVE_ENABLED, True)
        run_auto_archive(app)

        assert setting_service.get_int(AUTO_ARCHIVE_LAST_RUN_COUNT) == 2
        assert setting_service.get(AUTO_ARCHIVE_LAST_RUN_AT) is not None
        assert all(
            t.archived_at is not None
            for t in task_service.get_archived()
        )

    def test_on_tanpa_task_done_count_nol(self, app):
        setting_service.set(AUTO_ARCHIVE_ENABLED, True)
        run_auto_archive(app)
        assert setting_service.get_int(AUTO_ARCHIVE_LAST_RUN_COUNT) == 0


class TestSettingRoutes:
    """TC-13d: routes Pengaturan (PRG + proteksi)."""

    def test_pengaturan_tanpa_login_redirect(self, client):
        assert client.get("/pengaturan/").status_code == 302

    def test_pengaturan_render_toggle_dan_status(self, client, login_user):
        body = client.get("/pengaturan/").data.decode()
        assert 'role="switch"' in body
        assert "Tidak terjadwal" in body  # off + belum pernah jalan
        assert "Belum pernah berjalan" in body

    def test_toggle_on_persist_dan_prg(self, client, login_user):
        response = client.post(
            "/pengaturan/auto-archive", data={"enabled": "true"}, follow_redirects=False
        )
        assert response.status_code == 302
        assert "/pengaturan/" in response.headers["Location"]
        assert setting_service.get_bool(AUTO_ARCHIVE_ENABLED) is True

    def test_toggle_off_persist(self, client, login_user):
        setting_service.set(AUTO_ARCHIVE_ENABLED, True)
        client.post("/pengaturan/auto-archive", data={"enabled": "false"})
        assert setting_service.get_bool(AUTO_ARCHIVE_ENABLED) is False

    def test_sidebar_memuat_menu_pengaturan(self, client, login_user):
        body = client.get("/pengaturan/").data.decode()
        assert 'href="/pengaturan/"' in body
