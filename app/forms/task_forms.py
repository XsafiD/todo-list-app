"""Form Task."""
from flask_wtf import FlaskForm
from wtforms import DateTimeLocalField, SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional

from app.services.note_service import NOTE_MAX_LENGTH

PRIORITY_CHOICES = [("low", "Rendah"), ("medium", "Sedang"), ("high", "Tinggi")]
STATUS_CHOICES = [("todo", "Todo"), ("in_progress", "Sedang Dikerjakan"), ("done", "Selesai")]


def project_choices() -> list[tuple[str, str]]:
    """Pilihan project dari service (mock Phase 1) — dipasang di controller."""
    from app.services.project_service import project_service

    return [("", "Tanpa Project (Inbox)")] + [
        (str(p.id), p.name) for p in project_service.get_all()
    ]


class TaskForm(FlaskForm):
    """Dipakai untuk create & edit — choices project di-set di controller."""

    title = StringField("Judul Tugas", validators=[
        DataRequired(message="Judul tugas wajib diisi."),
        Length(min=1, max=500, message="Judul maksimal 500 karakter."),
    ])
    description = TextAreaField("Deskripsi", validators=[Optional()])
    assignee = StringField(
        "Penanggung Jawab",
        validators=[Optional(), Length(max=255, message="Penanggung jawab maksimal 255 karakter.")],
    )
    project_id = SelectField("Project", choices=[("", "Tanpa Project (Inbox)")], coerce=str)
    priority = SelectField("Prioritas", choices=PRIORITY_CHOICES, default="medium")
    status = SelectField("Status", choices=STATUS_CHOICES, default="todo")
    deadline = DateTimeLocalField("Deadline", format="%Y-%m-%dT%H:%M", validators=[Optional()])


class NoteForm(FlaskForm):
    """Catatan timeline proses — dipakai di halaman detail task."""

    content = TextAreaField(
        "Catatan",
        validators=[
            DataRequired(message="Catatan wajib diisi."),
            Length(max=NOTE_MAX_LENGTH, message=f"Catatan maksimal {NOTE_MAX_LENGTH} karakter."),
        ],
        render_kw={
            "rows": 3,
            "maxlength": NOTE_MAX_LENGTH,
            "placeholder": "Tulis catatan progres untuk tugas ini...",
        },
    )
