"""
controllers/setting_controller.py — Blueprint ``setting_bp``.

Routes (semua login_required):
  - GET  /pengaturan/             — halaman pengaturan (arsip otomatis)
  - POST /pengaturan/auto-archive — toggle arsip otomatis on/off
"""
from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.scheduler import next_auto_archive_run
from app.services.setting_service import (
    AUTO_ARCHIVE_ENABLED,
    AUTO_ARCHIVE_LAST_RUN_AT,
    AUTO_ARCHIVE_LAST_RUN_COUNT,
    setting_service,
)
from app.utils.decorators import login_required

setting_bp = Blueprint("setting", __name__, url_prefix="/pengaturan")


@setting_bp.route("/")
@login_required
def index():
    """Halaman pengaturan — status & toggle sistem otomatis."""
    last_run_raw = setting_service.get(AUTO_ARCHIVE_LAST_RUN_AT)
    last_run_at = None
    if last_run_raw:
        try:
            last_run_at = datetime.fromisoformat(last_run_raw)
        except ValueError:
            last_run_at = None
    return render_template(
        "setting/index.html",
        auto_archive_enabled=setting_service.get_bool(AUTO_ARCHIVE_ENABLED),
        auto_archive_next_run=next_auto_archive_run(),
        auto_archive_last_run=last_run_at,
        auto_archive_last_count=setting_service.get_int(AUTO_ARCHIVE_LAST_RUN_COUNT),
    )


@setting_bp.route("/auto-archive", methods=["POST"])
@login_required
def toggle_auto_archive():
    enabled = request.form.get("enabled", "false").lower() in {"1", "true", "yes"}
    setting_service.set(AUTO_ARCHIVE_ENABLED, enabled)
    flash(
        "Arsip otomatis diaktifkan — tugas selesai diarsipkan tiap 23:59."
        if enabled
        else "Arsip otomatis dinonaktifkan — arsipkan manual dari Kanban.",
        "success",
    )
    return redirect(url_for("setting.index"))
