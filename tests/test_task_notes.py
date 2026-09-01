"""tests/test_task_notes.py — TC: catatan timeline proses (service + route)."""
import pytest

from app.extensions import db
from app.models import TaskNote
from app.services.note_service import NOTE_MAX_LENGTH, note_service
from app.services.task_service import task_service


@pytest.fixture
def sample_task(app):
    return task_service.create(title="Riset kompetitor")


@pytest.fixture
def archived_task(app, sample_task):
    task_service.update_status(sample_task.id, "done")
    return task_service.archive(sample_task.id)


class TestNoteService:
    """TC: NoteService — add/delete/get + guard task terarsip."""

    def test_add_dan_urutan_terbaru_dulu(self, sample_task):
        pertama = note_service.add_note(sample_task.id, "Catatan pertama")
        kedua = note_service.add_note(sample_task.id, "Catatan kedua")
        notes = note_service.get_for_task(sample_task.id)
        assert [n.id for n in notes] == [kedua.id, pertama.id]

    def test_add_konten_dipangkas(self, sample_task):
        note = note_service.add_note(sample_task.id, "  Catatan bersih  ")
        assert note.content == "Catatan bersih"

    def test_add_kosong_valueerror(self, sample_task):
        with pytest.raises(ValueError, match="wajib diisi"):
            note_service.add_note(sample_task.id, "   ")

    def test_add_lebih_batas_valueerror(self, sample_task):
        with pytest.raises(ValueError, match="1000 karakter"):
            note_service.add_note(sample_task.id, "x" * (NOTE_MAX_LENGTH + 1))

    def test_add_task_tidak_ada_valueerror(self, app):
        with pytest.raises(ValueError, match="Tugas tidak ditemukan"):
            note_service.add_note(999, "catatan")

    def test_add_task_terarsip_ditolak(self, archived_task):
        with pytest.raises(ValueError, match="diarsipkan"):
            note_service.add_note(archived_task.id, "Terlambat")

    def test_delete_berhasil(self, sample_task):
        note = note_service.add_note(sample_task.id, "Hapus aku")
        note_service.delete_note(sample_task.id, note.id)
        assert note_service.get_for_task(sample_task.id) == []

    def test_delete_note_task_lain_valueerror(self, sample_task):
        other = task_service.create(title="Task lain")
        note = note_service.add_note(sample_task.id, "Milik task pertama")
        with pytest.raises(ValueError, match="Catatan tidak ditemukan"):
            note_service.delete_note(other.id, note.id)

    def test_delete_sampah_bersama_task(self, sample_task):
        note_service.add_note(sample_task.id, "Ikut terhapus")
        task_service.delete(sample_task.id)
        assert db.session.query(TaskNote).count() == 0


class TestNoteRoutes:
    """TC: route timeline — POST add/delete + render detail (login wajib)."""

    def test_tanpa_login_redirect(self, client, sample_task):
        resp = client.post(f"/tasks/{sample_task.id}/notes", data={"content": "x"})
        assert resp.status_code == 302
        assert "/login" in resp.headers["Location"]

    def test_detail_menampilkan_timeline(self, client, login_user, sample_task):
        note_service.add_note(sample_task.id, "Draft awal selesai")
        resp = client.get(f"/tasks/{sample_task.id}")
        assert resp.status_code == 200
        assert b"Timeline Proses" in resp.data
        assert b"Draft awal selesai" in resp.data
        assert b"Belum ada catatan" not in resp.data

    def test_detail_kosong_empty_state(self, client, login_user, sample_task):
        resp = client.get(f"/tasks/{sample_task.id}")
        assert b"Belum ada catatan" in resp.data

    def test_add_berhasil_redirect_dan_render(self, client, login_user, sample_task):
        resp = client.post(
            f"/tasks/{sample_task.id}/notes",
            data={"content": "Mulai riset"},
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert b"Mulai riset" in resp.data

    def test_add_kosong_flash_error(self, client, login_user, sample_task):
        resp = client.post(
            f"/tasks/{sample_task.id}/notes",
            data={"content": "  "},
            follow_redirects=True,
        )
        assert b"wajib diisi" in resp.data

    def test_add_task_terarsip_flash_error(self, client, login_user, archived_task):
        resp = client.post(
            f"/tasks/{archived_task.id}/notes",
            data={"content": "x"},
            follow_redirects=True,
        )
        assert b"diarsipkan" in resp.data

    def test_delete_berhasil(self, client, login_user, sample_task):
        note = note_service.add_note(sample_task.id, "Sementara")
        resp = client.post(
            f"/tasks/{sample_task.id}/notes/{note.id}/delete",
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert b"Sementara" not in resp.data

    def test_delete_note_task_lain_404(self, client, login_user, sample_task):
        other = task_service.create(title="Task lain")
        note = note_service.add_note(sample_task.id, "Milik task pertama")
        resp = client.post(f"/tasks/{other.id}/notes/{note.id}/delete")
        assert resp.status_code == 404
