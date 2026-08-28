"""
controllers/archive_controller.py — Blueprint ``archive_bp``.

Routes (semua login_required):
  - GET /arsip/  — daftar tugas terarsip (filter via query params)
"""
from flask import Blueprint, render_template, request

from app.services.project_service import project_service
from app.services.task_service import task_service
from app.utils.decorators import login_required

archive_bp = Blueprint("archive", __name__, url_prefix="/arsip")


@archive_bp.route("/")
@login_required
def index():
    """Daftar tugas terarsip — sort `archived_at` terbaru dulu."""
    project_id = request.args.get("project_id")
    filters: dict = {}
    if project_id and project_id.isdigit():
        filters["project_id"] = int(project_id)
    return render_template(
        "archive/list.html",
        tasks=task_service.get_archived(filters=filters),
        filters=filters,
        projects_all=project_service.get_all(),
    )
