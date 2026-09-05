"""
controllers/project_controller.py — Blueprint ``project_bp``.

Routes (semua login_required):
  - GET/POST /projects/                — daftar / (POST tidak dipakai)
  - GET/POST /projects/create          — tambah baru
  - GET      /projects/<id>            — detail
  - GET/POST /projects/<id>/edit       — edit
  - POST     /projects/<id>/archive    — arsipkan / pulihkan
  - POST     /projects/<id>/delete     — hapus
"""
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from app.forms.project_forms import ProjectForm
from app.services.project_service import project_service
from app.services.task_service import task_service
from app.utils.decorators import login_required

project_bp = Blueprint("project", __name__, url_prefix="/projects")


def _form_payload(form: ProjectForm) -> dict:
    """Ambil data form tanpa token CSRF."""
    return {k: v for k, v in form.data.items() if k != "csrf_token"}


@project_bp.route("/")
@login_required
def index():
    all_projects = project_service.get_all(include_archived=True)
    active = [p for p in all_projects if not p.archived]
    archived = [p for p in all_projects if p.archived]
    return render_template("project/list.html", projects=active, archived_projects=archived)


@project_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = ProjectForm()
    if form.validate_on_submit():
        try:
            project = project_service.create(**_form_payload(form))
            flash(f"Project '{project.name}' berhasil dibuat.", "success")
            return redirect(url_for("project.index"))
        except ValueError as err:
            flash(str(err), "error")
    return render_template("project/create.html", form=form)


@project_bp.route("/<int:project_id>")
@login_required
def detail(project_id: int):
    project = project_service.get_by_id(project_id)
    if project is None:
        abort(404)
    filters = {"project_id": project_id}
    tasks = task_service.get_all(filters=filters)
    archived_tasks = task_service.get_archived(filters=filters)
    return render_template(
        "project/detail.html", project=project, tasks=tasks, archived_tasks=archived_tasks
    )


@project_bp.route("/<int:project_id>/edit", methods=["GET", "POST"])
@login_required
def edit(project_id: int):
    project = project_service.get_by_id(project_id)
    if project is None:
        abort(404)
    form = ProjectForm(obj=project)
    if form.validate_on_submit():
        try:
            project_service.update(project_id, **_form_payload(form))
            flash(f"Project '{project.name}' berhasil diperbarui.", "success")
            return redirect(url_for("project.detail", project_id=project_id))
        except ValueError as err:
            flash(str(err), "error")
    return render_template("project/edit.html", form=form, project=project)


@project_bp.route("/<int:project_id>/archive", methods=["POST"])
@login_required
def archive(project_id: int):
    archived = request.form.get("archived", "true").lower() in {"1", "true", "yes"}
    try:
        project = project_service.set_archived(project_id, archived)
    except ValueError:
        abort(404)
    verb = "diarsipkan" if archived else "dipulihkan"
    flash(f"Project '{project.name}' berhasil {verb}.", "success")
    return redirect(url_for("project.index"))


@project_bp.route("/<int:project_id>/delete", methods=["POST"])
@login_required
def delete(project_id: int):
    try:
        project = project_service.delete(project_id)
    except ValueError:
        abort(404)
    flash(f"Project '{project.name}' dihapus. Tugas di dalamnya kini tanpa project.", "success")
    return redirect(url_for("project.index"))
