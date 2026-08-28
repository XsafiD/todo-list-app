"""
controllers/main_controller.py — Blueprint ``main_bp``.

Routes:
  - GET  /        — dashboard (login_required)
  - GET  /health  — health check (public)
"""
from datetime import datetime

from flask import Blueprint, render_template

from app.services.project_service import project_service
from app.services.task_service import task_service
from app.utils.decorators import login_required

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@login_required
def dashboard():
    projects = project_service.get_all()
    total_projects, active_projects = project_service.count_all()
    stats = task_service.get_stats(
        total_projects=total_projects,
        active_projects=active_projects,
    )
    return render_template(
        "dashboard/index.html",
        stats=stats,
        projects=projects,
        recent_tasks=task_service.get_recent(limit=5),
        now=datetime.now(),
    )


@main_bp.route("/health")
def health():
    """Health check — public, tanpa data sensitif."""
    return {"status": "ok", "service": "dashboardku"}
