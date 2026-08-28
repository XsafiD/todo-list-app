"""tests/test_stats.py — TC: agregasi stats dashboard di database."""
from datetime import datetime, timedelta

from app.services.project_service import project_service
from app.services.task_service import task_service


class TestStatsDashboard:
    """TC-11: get_stats akurat terhadap data."""

    def test_stats_kosong(self, app):
        total, active = project_service.count_all()
        stats = task_service.get_stats(total_projects=total, active_projects=active)
        assert stats.total_tasks == 0
        assert stats.active_tasks == 0
        assert stats.overdue_tasks == 0

    def test_stats_hitung_lengkap(self, app):
        project = project_service.create(name="P", color="#3B82F6")
        task_service.create(title="Aktif", project_id=project.id)
        task_service.create(title="Selesai", status="done")
        task_service.create(
            title="Terlambat",
            deadline=datetime.now() - timedelta(days=1),  # sudah lewat
        )

        total, active = project_service.count_all()
        stats = task_service.get_stats(total_projects=total, active_projects=active)

        assert stats.total_tasks == 3
        assert stats.completed_tasks == 1
        assert stats.active_tasks == 2
        assert stats.overdue_tasks == 1
        assert stats.total_projects == 1
        assert stats.active_projects == 1

    def test_task_done_tidak_dihitung_overdue(self, app):
        task_service.create(
            title="Telat tapi selesai",
            deadline=datetime.now() - timedelta(days=2),
            status="done",
        )
        stats = task_service.get_stats()
        assert stats.overdue_tasks == 0
