"""
controllers/task_controller.py — Blueprint ``task_bp``.

Routes (semua login_required):
  - GET/POST /tasks/                — daftar (filter via query params)
  - GET/POST /tasks/create          — tambah baru (?project_id= preselect)
  - GET      /tasks/<id>            — detail (+ timeline catatan)
  - GET/POST /tasks/<id>/edit       — edit
  - POST     /tasks/<id>/complete   — toggle selesai
  - POST     /tasks/<id>/status     — ubah status (drag & drop kanban, JSON)
  - POST     /tasks/<id>/archive    — arsipkan task done
  - POST     /tasks/<id>/unarchive  — keluarkan dari arsip
  - POST     /tasks/<id>/delete     — hapus (next= kembali ke halaman asal)
  - POST     /tasks/<id>/notes      — tambah catatan timeline
  - POST     /tasks/<id>/notes/<note_id>/delete — hapus catatan timeline
  - GET      /tasks/kanban          — board kanban 3 kolom per status
"""
from flask import Blueprint, abort, flash, jsonify, redirect, render_template, request, url_for

from app.forms.task_forms import STATUS_CHOICES, PRIORITY_CHOICES, NoteForm, TaskForm, project_choices
from app.services.note_service import note_service
from app.services.project_service import project_service
from app.services.task_service import task_service
from app.utils.decorators import login_required

task_bp = Blueprint("task", __name__, url_prefix="/tasks")

_ALLOWED_STATUS = {value for value, _ in STATUS_CHOICES}
_ALLOWED_PRIORITY = {value for value, _ in PRIORITY_CHOICES}

# Kolom papan kanban — urutan tampilan board (key = nilai enum TaskStatus)
KANBAN_COLUMNS = [
    ("todo", "Todo"),
    ("in_progress", "Proses"),
    ("done", "Selesai"),
]


def _get_task_or_404(public_id: str):
    task = task_service.get_by_public_id(public_id)
    if task is None:
        abort(404)
    return task


def _parse_filters() -> dict:
    """Ambil filter dari query args — nilai tak dikenal diabaikan."""
    filters: dict = {}
    status = request.args.get("status")
    if status in _ALLOWED_STATUS:
        filters["status"] = status
    priority = request.args.get("priority")
    if priority in _ALLOWED_PRIORITY:
        filters["priority"] = priority
    project_id = request.args.get("project_id")
    if project_id and project_id.isdigit():
        filters["project_id"] = int(project_id)
    return filters


def _form_payload(form: TaskForm) -> dict:
    """Ambil data form tanpa token CSRF."""
    return {k: v for k, v in form.data.items() if k != "csrf_token"}


def _wants_json() -> bool:
    """Request AJAX dari modul JS mengirim header ini (10-api-response.md #4)."""
    return request.headers.get("X-Requested-With") == "fetch"


def _safe_next(fallback: str) -> str:
    """URL tujuan dari form field `next` — hanya path relatif (anti open redirect)."""
    next_url = request.form.get("next") or ""
    if next_url.startswith("/") and not next_url.startswith("//"):
        return next_url
    return fallback


@task_bp.route("/")
@login_required
def index():
    filters = _parse_filters()
    tasks = task_service.get_all(filters=filters)
    return render_template(
        "task/list.html",
        tasks=tasks,
        filters=filters,
        status_choices=STATUS_CHOICES,
        priority_choices=PRIORITY_CHOICES,
        projects_all=project_service.get_all(),
    )


@task_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = TaskForm()
    form.project_id.choices = project_choices()
    preselect = request.args.get("project_id", "")
    if request.method == "GET" and preselect:
        form.project_id.data = preselect
    if form.validate_on_submit():
        try:
            task = task_service.create(**_form_payload(form))
            flash(f"Tugas '{task.title}' berhasil dibuat.", "success")
            return redirect(url_for("task.index"))
        except ValueError as err:
            flash(str(err), "error")
    return render_template("task/create.html", form=form)


@task_bp.route("/<string:task_id>")
@login_required
def detail(task_id: str):
    task = _get_task_or_404(task_id)
    return render_template(
        "task/detail.html",
        task=task,
        notes=note_service.get_for_task(task.id),
        note_form=NoteForm(),
    )


@task_bp.route("/<string:task_id>/edit", methods=["GET", "POST"])
@login_required
def edit(task_id: str):
    task = _get_task_or_404(task_id)
    form = TaskForm(obj=task)
    form.project_id.choices = project_choices()
    form.priority.data = task.priority
    form.status.data = task.status
    form.project_id.data = str(task.project_id) if task.project_id else ""

    if form.validate_on_submit():
        try:
            task_service.update(task.id, **_form_payload(form))
            flash(f"Tugas '{task.title}' berhasil diperbarui.", "success")
            return redirect(url_for("task.detail", task_id=task.public_id))
        except ValueError as err:
            flash(str(err), "error")
    return render_template("task/edit.html", form=form, task=task)


@task_bp.route("/<string:task_id>/complete", methods=["POST"])
@login_required
def complete(task_id: str):
    task = _get_task_or_404(task_id)
    try:
        task_obj = task_service.toggle_complete(task.id)
    except ValueError:
        if _wants_json():
            return jsonify(status="error", error="not_found", message="Tugas tidak ditemukan."), 404
        abort(404)
    verb = "ditandai selesai" if task_obj.status.value == "done" else "dibuka kembali"
    message = f"Tugas '{task_obj.title}' {verb}."
    if _wants_json():
        return jsonify(
            status="ok",
            data={"id": task_obj.id, "title": task_obj.title, "status": task_obj.status.value},
            message=message,
        )
    flash(message, "success")
    return redirect(request.form.get("next") or url_for("task.detail", task_id=task.public_id))


@task_bp.route("/<string:task_id>/notes", methods=["POST"])
@login_required
def add_note(task_id: str):
    """Tambah catatan timeline — task terarsip ditolak di service."""
    task = _get_task_or_404(task_id)
    form = NoteForm()
    if form.validate_on_submit():
        try:
            note_service.add_note(task.id, form.content.data)
            flash("Catatan ditambahkan ke timeline.", "success")
        except ValueError as err:
            flash(str(err), "error")
    else:
        flash(form.content.errors[0] if form.content.errors else "Catatan tidak valid.", "error")
    return redirect(url_for("task.detail", task_id=task.public_id))


@task_bp.route("/<string:task_id>/notes/<int:note_id>/delete", methods=["POST"])
@login_required
def delete_note(task_id: str, note_id: int):
    task = _get_task_or_404(task_id)
    try:
        note_service.delete_note(task.id, note_id)
    except ValueError:
        abort(404)
    flash("Catatan timeline dihapus.", "success")
    return redirect(url_for("task.detail", task_id=task.public_id))


@task_bp.route("/kanban")
@login_required
def kanban():
    """Board kanban — 3 kolom per status, task dikelompokkan di controller."""
    grouped: dict[str, list] = {key: [] for key, _ in KANBAN_COLUMNS}
    for task in task_service.get_all():
        grouped.setdefault(task.status, []).append(task)
    return render_template("task/kanban.html", columns=KANBAN_COLUMNS, grouped=grouped)


@task_bp.route("/<string:task_id>/status", methods=["POST"])
@login_required
def update_status(task_id: str):
    task = _get_task_or_404(task_id)
    payload = request.get_json(silent=True) or {}
    status = payload.get("status", "")
    if status not in _ALLOWED_STATUS:
        message = "Status harus todo, in_progress, atau done."
        if _wants_json():
            return jsonify(status="error", error="invalid_status", message=message), 400
        flash(message, "error")
        return redirect(url_for("task.kanban"))
    try:
        task_obj = task_service.update_status(task.id, status)
    except ValueError:
        if _wants_json():
            return jsonify(status="error", error="not_found", message="Tugas tidak ditemukan."), 404
        abort(404)
    message = f"Status tugas '{task_obj.title}' diperbarui."
    if _wants_json():
        return jsonify(
            status="ok",
            data={"id": task_obj.id, "title": task_obj.title, "status": task_obj.status.value},
            message=message,
        )
    flash(message, "success")
    return redirect(url_for("task.kanban"))


@task_bp.route("/<string:task_id>/archive", methods=["POST"])
@login_required
def archive(task_id: str):
    task = _get_task_or_404(task_id)
    try:
        task_obj = task_service.archive(task.id)
    except ValueError as err:
        flash(str(err), "error")
        return redirect(url_for("task.kanban"))
    flash(f"Tugas '{task_obj.title}' dipindahkan ke Arsip.", "success")
    return redirect(_safe_next(url_for("task.kanban")))


@task_bp.route("/<string:task_id>/unarchive", methods=["POST"])
@login_required
def unarchive(task_id: str):
    task = _get_task_or_404(task_id)
    try:
        task_obj = task_service.unarchive(task.id)
    except ValueError:
        abort(404)
    flash(f"Tugas '{task_obj.title}' dikeluarkan dari Arsip — kembali ke kolom Selesai.", "success")
    return redirect(_safe_next(url_for("archive.index")))


@task_bp.route("/<string:task_id>/delete", methods=["POST"])
@login_required
def delete(task_id: str):
    task = _get_task_or_404(task_id)
    try:
        task_obj = task_service.delete(task.id)
    except ValueError:
        abort(404)
    flash(f"Tugas '{task_obj.title}' dihapus.", "success")
    return redirect(_safe_next(url_for("task.index")))
