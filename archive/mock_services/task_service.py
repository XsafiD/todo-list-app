"""TaskService — business logic Task + stats dashboard.

PHASE 1 (view-first): sumber data MOCK di module ini — belum query database.
Field display (deadline_state, project_name, dll.) precomputed di service
sesuai 04-view.md #5 (hitungan berat jangan di template).
"""
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(frozen=True)
class TaskView:
    """DTO tampilan task."""
    id: int
    project_id: int | None
    project_name: str | None
    project_color: str | None
    title: str
    description: str | None
    priority: str
    status: str
    deadline: datetime | None
    deadline_state: str  # "" | "upcoming" | "today" | "overdue"
    deadline_label: str  # "2 hari lagi", "Hari ini 14:00", "Terlambat 1 hari", ""
    completed_at: datetime | None
    created_at: datetime


@dataclass(frozen=True)
class StatsView:
    total_tasks: int
    active_tasks: int
    completed_tasks: int
    overdue_tasks: int
    total_projects: int
    active_projects: int


def _deadline_state(deadline: datetime | None, status: str, now: datetime) -> str:
    if deadline is None or status == "done":
        return ""
    if deadline < now:
        return "overdue"
    if deadline.date() == now.date():
        return "today"
    return "upcoming"


def _deadline_label(state: str, deadline: datetime | None, now: datetime) -> str:
    """Label ringkas untuk badge deadline — precompute di service."""
    if deadline is None:
        return ""
    if state == "overdue":
        diff = now - deadline
        if diff.days >= 1:
            return f"Terlambat {diff.days} hari"
        hours = max(diff.seconds // 3600, 1)
        return f"Terlambat {hours} jam"
    if state == "today":
        return f"Hari ini {deadline.strftime('%H:%M')}"
    diff = deadline - now
    if diff.days >= 1:
        return f"{diff.days} hari lagi"
    hours = max(diff.seconds // 3600, 1)
    return f"{hours} jam lagi"


def _build_mock_tasks() -> list[TaskView]:
    """Mock dinamis — deadline relatif terhadap sekarang agar state selalu relevan."""
    now = datetime.now()
    raw = [
        # (id, project_id, title, desc, priority, status, deadline_offset, completed_offset)
        (1, 1, "Finalisasi laporan bulanan",
         "Rangkum metrik Juli, ekspor ke PDF, kirim ke tim.",
         "high", "in_progress", ("today", 14, 0), None),
        (2, 1, "Review PR tim frontend",
         "PR #142 — cek komponen form dan test coverage.",
         "medium", "todo", ("past", 17, 0), None),
        (3, 2, "Panggil dokter gigi",
         "Jadwalkan kontrol 6 bulanan.",
         "low", "todo", ("future_day", 2, 0), None),
        (4, 3, "Belajar modul SQLAlchemy 2.0",
         "Bab relationship & selectin loading, coba langsung di sandbox.",
         "medium", "in_progress", ("future_day", 5, 0), None),
        (5, 4, "Rangkum ide aplikasi catatan",
         None,
         "low", "done", None, ("past_day", 1)),
        (6, 2, "Setup backup otomatis laptop",
         "Restic + cron mingguan ke disk eksternal.",
         "high", "todo", ("future_hour", 3), None),
    ]
    projects = {1: ("Pekerjaan", "#3B82F6"), 2: ("Pribadi", "#10B981"),
                3: ("Belajar", "#14B8A6"), 4: ("Ide & Riset", "#EC4899")}

    def _resolve(offset):
        if offset is None:
            return None
        kind, *nums = offset
        if kind == "today":
            return now.replace(hour=nums[0], minute=nums[1], second=0, microsecond=0)
        if kind == "past":
            return (now - timedelta(days=1)).replace(hour=nums[0], minute=nums[1], second=0, microsecond=0)
        if kind == "past_day":
            return now - timedelta(days=nums[0])
        if kind == "future_day":
            return now + timedelta(days=nums[0])
        if kind == "future_hour":
            return now + timedelta(hours=nums[0])
        return None

    views = []
    for tid, pid, title, desc, priority, status, deadline_off, completed_off in raw:
        project = projects.get(pid)
        deadline = _resolve(deadline_off)
        state = _deadline_state(deadline, status, now)
        views.append(TaskView(
            id=tid,
            project_id=pid,
            project_name=project[0] if project else None,
            project_color=project[1] if project else None,
            title=title,
            description=desc,
            priority=priority,
            status=status,
            deadline=deadline,
            deadline_state=state,
            deadline_label=_deadline_label(state, deadline, now),
            completed_at=_resolve_completed(completed_off, now),
            created_at=now - timedelta(days=len(raw) - tid),
        ))
    return views


def _resolve_completed(offset, now: datetime) -> datetime | None:
    if offset is None:
        return None
    return now - timedelta(days=offset[1])


class TaskService:
    """CRUD + aturan bisnis Task (mock, Phase 1)."""

    def get_all(self, filters: dict | None = None) -> list[TaskView]:
        """Filter: status, priority, project_id. Sort: aktif dulu, lalu terbaru."""
        filters = filters or {}
        tasks = _build_mock_tasks()

        status = filters.get("status")
        if status:
            tasks = [t for t in tasks if t.status == status]
        priority = filters.get("priority")
        if priority:
            tasks = [t for t in tasks if t.priority == priority]
        project_id = filters.get("project_id")
        if project_id is not None:
            tasks = [t for t in tasks if t.project_id == project_id]

        return sorted(tasks, key=lambda t: (t.status == "done", -t.id))

    def get_by_id(self, task_id: int) -> TaskView | None:
        return next((t for t in _build_mock_tasks() if t.id == task_id), None)

    def get_recent(self, limit: int = 5) -> list[TaskView]:
        return self.get_all()[:limit]

    def get_stats(self, total_projects: int, active_projects: int) -> StatsView:
        tasks = _build_mock_tasks()
        now = datetime.now()
        done = [t for t in tasks if t.status == "done"]
        overdue = [t for t in tasks if _deadline_state(t.deadline, t.status, now) == "overdue"]
        return StatsView(
            total_tasks=len(tasks),
            active_tasks=len(tasks) - len(done),
            completed_tasks=len(done),
            overdue_tasks=len(overdue),
            total_projects=total_projects,
            active_projects=active_projects,
        )

    # ── Aksi tulis: simulasi (view-first) ──
    def create(self, **data) -> None:
        """Simulasi — belum persist (Phase 2: insert ORM + sync Day-H reminder)."""

    def update(self, task_id: int, **data) -> None:
        """Simulasi — belum persist."""

    def toggle_complete(self, task_id: int) -> None:
        """Simulasi — belum persist (Phase 2: delegasi task.toggle_complete())."""

    def delete(self, task_id: int) -> None:
        """Simulasi — belum persist."""


task_service = TaskService()
