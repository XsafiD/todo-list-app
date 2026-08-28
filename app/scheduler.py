"""Background scheduler — arsip otomatis harian (APScheduler BackgroundScheduler).

Job ``auto_archive`` jalan tiap 23:59 WAKTU LOKAL (konsisten konvensi deadline).
Saat jalan ia membaca setting ``auto_archive_enabled`` — off = no-op, jadi
toggle dari halaman Pengaturan langsung efektif tanpa restart.

Guard double-start: Werkzeug debug reloader men-spawn proses parent + child;
hanya child (WERKZEUG_RUN_MAIN=true) yang boleh start scheduler.
"""
import logging
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from flask import Flask

from app.services.setting_service import (
    AUTO_ARCHIVE_ENABLED,
    AUTO_ARCHIVE_LAST_RUN_AT,
    AUTO_ARCHIVE_LAST_RUN_COUNT,
    setting_service,
)
from app.services.task_service import task_service

logger = logging.getLogger(__name__)

AUTO_ARCHIVE_JOB_ID = "auto_archive"
AUTO_ARCHIVE_HOUR = 23
AUTO_ARCHIVE_MINUTE = 59

_scheduler: BackgroundScheduler | None = None


def run_auto_archive(app: Flask) -> None:
    """Eksekusi job arsip otomatis — dipanggil scheduler; testable langsung.

    Baca toggle SAAT runtime (bukan saat start). Catat hasil run ke settings
    untuk ditampilkan di halaman Pengaturan.
    """
    with app.app_context():
        if not setting_service.get_bool(AUTO_ARCHIVE_ENABLED):
            return
        count = task_service.archive_all_completed()
        now = datetime.now()  # lokal — konsisten konvensi tampilan deadline
        setting_service.set(AUTO_ARCHIVE_LAST_RUN_AT, now.isoformat())
        setting_service.set(AUTO_ARCHIVE_LAST_RUN_COUNT, count)
        if count:
            logger.info("Auto-archive: %d task diarsipkan.", count)


def init_scheduler(app: Flask) -> None:
    """Start scheduler sekali per proses — no-op bila sudah jalan/di-disable."""
    global _scheduler
    if _scheduler is not None:
        return
    if not app.config.get("SCHEDULER_ENABLED", False):
        return
    _scheduler = BackgroundScheduler(daemon=True)
    _scheduler.add_job(
        run_auto_archive,
        trigger=CronTrigger(hour=AUTO_ARCHIVE_HOUR, minute=AUTO_ARCHIVE_MINUTE),
        args=[app],
        id=AUTO_ARCHIVE_JOB_ID,
        name="Arsip otomatis harian",
        replace_existing=True,
    )
    _scheduler.start()
    logger.info("Scheduler aktif — job %s tiap %02d:%02d lokal.", AUTO_ARCHIVE_JOB_ID, AUTO_ARCHIVE_HOUR, AUTO_ARCHIVE_MINUTE)


def next_auto_archive_run() -> datetime | None:
    """Jadwal run berikutnya — None bila scheduler tidak jalan (test/off)."""
    if _scheduler is None:
        return None
    job = _scheduler.get_job(AUTO_ARCHIVE_JOB_ID)
    return job.next_run_time if job else None
