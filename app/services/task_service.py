"""TaskService — business logic Task + stats (ORM, Phase 2).

Kontrak return: DTO `TaskView` untuk tampilan (deadline state/label
precomputed), objek `Task` untuk operasi tulis. Error kontrak: validasi
gagal → `raise ValueError(pesan)`.

Konvensi waktu: logika tampilan deadline (state/label/stats overdue)
memakai waktu LOKAL (`datetime.now()`) agar konsisten dengan input user
di form; `completed_at` memakai `utcnow` mengikuti data lama. Unifikasi
timezone penuh menyusul di Phase 4 (notifikasi).
"""
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import case, func, select
from sqlalchemy.orm import joinedload

from app.extensions import db
from app.models import Project, Reminder, ReminderType, Task, TaskPriority, TaskStatus

PRIORITY_VALUES = {p.value for p in TaskPriority}
STATUS_VALUES = {s.value for s in TaskStatus}


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
    archived_at: datetime | None
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


def _to_view(task: Task, now: datetime) -> TaskView:
    status = task.status.value
    state = _deadline_state(task.deadline, status, now)
    return TaskView(
        id=task.id,
        project_id=task.project_id,
        project_name=task.project.name if task.project else None,
        project_color=task.project.color if task.project else None,
        title=task.title,
        description=task.description,
        priority=task.priority.value,
        status=status,
        deadline=task.deadline,
        deadline_state=state,
        deadline_label=_deadline_label(state, task.deadline, now),
        completed_at=task.completed_at,
        archived_at=task.archived_at,
        created_at=task.created_at,
    )


def _sync_day_h_reminder(task: Task) -> None:
    """Pastikan reminder Day-H ada iff task punya deadline (yang sudah terkirim tidak dihapus).

    Adaptasi dari archive/fastapi_api/routes/tasks.py — dipanggil sebelum commit.
    """
    day_h = db.session.scalar(
        select(Reminder).where(
            Reminder.task_id == task.id,
            Reminder.reminder_type == ReminderType.DAY_H,
        )
    )
    if task.deadline is not None and day_h is None:
        db.session.add(Reminder(task_id=task.id, reminder_type=ReminderType.DAY_H))
    elif task.deadline is None and day_h is not None and not day_h.sent:
        db.session.delete(day_h)


def _resolve_project_id(project_id) -> int | None:
    """Terima None/""/str/int → int | None; project tak ada → ValueError."""
    if project_id in (None, ""):
        return None
    try:
        pid = int(project_id)
    except (TypeError, ValueError):
        raise ValueError("Project tidak valid.") from None
    if db.session.get(Project, pid) is None:
        raise ValueError("Project tidak ditemukan.")
    return pid


class TaskService:
    """CRUD + aturan bisnis Task."""

    # ── Read ──
    def get_all(self, filters: dict | None = None, limit: int | None = None) -> list[TaskView]:
        """Task AKTIF (belum terarsip). Filter: status, priority, project_id.

        Sort: aktif dulu, lalu terbaru.
        """
        now = datetime.now()
        query = Task.query.options(joinedload(Task.project)).filter(  # anti N+1 (17-performance #3)
            Task.archived_at.is_(None)
        )
        filters = filters or {}

        if filters.get("status"):
            query = query.filter(Task.status == TaskStatus(filters["status"]))
        if filters.get("priority"):
            query = query.filter(Task.priority == TaskPriority(filters["priority"]))
        project_id = filters.get("project_id")
        if project_id is not None:
            query = query.filter(Task.project_id == project_id)

        query = query.order_by(
            case((Task.status == TaskStatus.DONE, 1), else_=0),
            Task.created_at.desc(),
            Task.id.desc(),
        )
        if limit:
            query = query.limit(limit)
        return [_to_view(t, now) for t in query.all()]

    def get_archived(self, filters: dict | None = None) -> list[TaskView]:
        """Task TERARSIP — sort `archived_at` terbaru dulu. Filter: project_id."""
        now = datetime.now()
        query = Task.query.options(joinedload(Task.project)).filter(
            Task.archived_at.is_not(None)
        )
        filters = filters or {}

        project_id = filters.get("project_id")
        if project_id is not None:
            query = query.filter(Task.project_id == project_id)

        query = query.order_by(Task.archived_at.desc(), Task.id.desc())
        return [_to_view(t, now) for t in query.all()]

    def get_by_id(self, task_id: int) -> TaskView | None:
        task = (
            Task.query.options(joinedload(Task.project))
            .filter_by(id=task_id)
            .first()
        )
        if task is None:
            return None
        return _to_view(task, datetime.now())

    def get_recent(self, limit: int = 5) -> list[TaskView]:
        return self.get_all(limit=limit)

    def get_stats(self, total_projects: int = 0, active_projects: int = 0) -> StatsView:
        """Agregasi di database (17-performance #1/#2) — bukan load semua row."""
        now = datetime.now()
        total = db.session.scalar(select(func.count(Task.id))) or 0
        done = db.session.scalar(
            select(func.count(Task.id)).where(Task.status == TaskStatus.DONE)
        ) or 0
        overdue = db.session.scalar(
            select(func.count(Task.id)).where(
                Task.deadline.is_not(None),
                Task.deadline < now,
                Task.status != TaskStatus.DONE,
            )
        ) or 0
        return StatsView(
            total_tasks=total,
            active_tasks=total - done,
            completed_tasks=done,
            overdue_tasks=overdue,
            total_projects=total_projects,
            active_projects=active_projects,
        )

    # ── Validasi (multi-layer: border form + sini — 16-security.md #4) ──
    def _validate(self, title: str, priority: str, status: str) -> None:
        if not title or not title.strip():
            raise ValueError("Judul tugas wajib diisi.")
        if len(title.strip()) > 500:
            raise ValueError("Judul tugas maksimal 500 karakter.")
        if priority not in PRIORITY_VALUES:
            raise ValueError("Prioritas harus low, medium, atau high.")
        if status not in STATUS_VALUES:
            raise ValueError("Status harus todo, in_progress, atau done.")

    # ── Write ──
    def create(
        self,
        title: str,
        description: str | None = None,
        project_id=None,
        priority: str = "medium",
        status: str = "todo",
        deadline: datetime | None = None,
    ) -> Task:
        self._validate(title, priority, status)
        task = Task(
            title=title.strip(),
            description=(description or "").strip() or None,
            project_id=_resolve_project_id(project_id),
            priority=TaskPriority(priority),
            deadline=deadline,
        )
        task.apply_status(TaskStatus(status))
        db.session.add(task)
        db.session.flush()  # ID tersedia untuk relasi reminder (03-service #6)
        _sync_day_h_reminder(task)
        db.session.commit()
        return task

    def update(
        self,
        task_id: int,
        title: str,
        description: str | None = None,
        project_id=None,
        priority: str = "medium",
        status: str = "todo",
        deadline: datetime | None = None,
    ) -> Task:
        task = db.session.get(Task, task_id)
        if task is None:
            raise ValueError("Tugas tidak ditemukan.")
        self._validate(title, priority, status)

        task.title = title.strip()
        task.description = (description or "").strip() or None
        task.project_id = _resolve_project_id(project_id)
        task.priority = TaskPriority(priority)
        task.deadline = deadline
        task.apply_status(TaskStatus(status))  # state machine jaga completed_at
        _sync_day_h_reminder(task)
        db.session.commit()
        return task

    def update_status(self, task_id: int, status: str) -> Task:
        """Ubah status saja (kanban) — delegasi state machine (03-service #5).

        Args:
            task_id: ID task.
            status: "todo" | "in_progress" | "done".

        Returns:
            Objek Task yang sudah di-commit.

        Raises:
            ValueError: task tidak ditemukan atau status tidak dikenal.
        """
        if status not in STATUS_VALUES:
            raise ValueError("Status harus todo, in_progress, atau done.")
        task = db.session.get(Task, task_id)
        if task is None:
            raise ValueError("Tugas tidak ditemukan.")
        task.apply_status(TaskStatus(status))  # state machine jaga completed_at
        db.session.commit()
        return task

    def toggle_complete(self, task_id: int) -> Task:
        task = db.session.get(Task, task_id)
        if task is None:
            raise ValueError("Tugas tidak ditemukan.")
        task.toggle_complete()  # delegasi state machine model
        db.session.commit()
        return task

    def archive(self, task_id: int) -> Task:
        """Arsipkan task done — delegasi state machine (03-service #5).

        Args:
            task_id: ID task.

        Returns:
            Objek Task yang sudah di-commit.

        Raises:
            ValueError: task tidak ditemukan atau bukan berstatus done.
        """
        task = db.session.get(Task, task_id)
        if task is None:
            raise ValueError("Tugas tidak ditemukan.")
        task.archive()
        db.session.commit()
        return task

    def unarchive(self, task_id: int) -> Task:
        """Keluarkan task dari arsip — status tetap done.

        Args:
            task_id: ID task.

        Returns:
            Objek Task yang sudah di-commit.

        Raises:
            ValueError: task tidak ditemukan.
        """
        task = db.session.get(Task, task_id)
        if task is None:
            raise ValueError("Tugas tidak ditemukan.")
        task.unarchive()
        db.session.commit()
        return task

    def delete(self, task_id: int) -> Task:
        task = db.session.get(Task, task_id)
        if task is None:
            raise ValueError("Tugas tidak ditemukan.")
        db.session.delete(task)
        db.session.commit()
        return task


task_service = TaskService()
