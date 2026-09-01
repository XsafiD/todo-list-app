"""NoteService — business logic TaskNote (timeline proses di detail task)."""
from sqlalchemy import select

from app.extensions import db
from app.models import Task, TaskNote

#: Batas panjang satu catatan — dipakai juga NoteForm (05-form.md #6).
NOTE_MAX_LENGTH = 1000


class NoteService:
    """Catatan timeline task — append-only (tambah + hapus, tanpa edit)."""

    def get_for_task(self, task_id: int) -> list[TaskNote]:
        """Catatan milik task — terbaru dulu (id desc sebagai tiebreaker
        karena created_at beresolusi detik)."""
        return list(
            db.session.scalars(
                select(TaskNote)
                .where(TaskNote.task_id == task_id)
                .order_by(TaskNote.created_at.desc(), TaskNote.id.desc())
            ).all()
        )

    def add_note(self, task_id: int, content: str | None) -> TaskNote:
        """Tambah catatan ke timeline task.

        Args:
            task_id: ID task tujuan.
            content: isi catatan (di-strip; maksimal NOTE_MAX_LENGTH karakter).

        Returns:
            Objek TaskNote yang sudah di-commit.

        Raises:
            ValueError: task tidak ada, task sudah diarsipkan, atau konten
                kosong/melebihi batas panjang.
        """
        task = db.session.get(Task, task_id)
        if task is None:
            raise ValueError("Tugas tidak ditemukan.")
        if task.archived_at is not None:
            raise ValueError("Tugas sudah diarsipkan — timeline terkunci.")
        content = (content or "").strip()
        if not content:
            raise ValueError("Catatan wajib diisi.")
        if len(content) > NOTE_MAX_LENGTH:
            raise ValueError(f"Catatan maksimal {NOTE_MAX_LENGTH} karakter.")
        note = TaskNote(task_id=task_id, content=content)
        db.session.add(note)
        db.session.commit()
        return note

    def delete_note(self, task_id: int, note_id: int) -> TaskNote:
        """Hapus catatan — scoped ke task (note milik task lain = tidak ada).

        Args:
            task_id: ID task pemilik (dari URL, anti cross-task delete).
            note_id: ID catatan.

        Returns:
            Objek TaskNote yang dihapus.

        Raises:
            ValueError: catatan tidak ditemukan pada task tersebut.
        """
        note = db.session.get(TaskNote, note_id)
        if note is None or note.task_id != task_id:
            raise ValueError("Catatan tidak ditemukan.")
        db.session.delete(note)
        db.session.commit()
        return note


note_service = NoteService()
