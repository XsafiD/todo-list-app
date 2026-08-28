"""ProjectService — business logic Project.

PHASE 1 (view-first): sumber data MOCK di module ini — belum query database.
Kontrak method tetap sama sehingga Phase 2 cukup mengganti sumber data ke ORM.
Aksi tulis (create/update/archive/delete) adalah simulasi: tidak persist.
"""
from dataclasses import dataclass
from datetime import datetime, timedelta

from app.services.task_service import task_service


@dataclass(frozen=True)
class ProjectView:
    """DTO tampilan project — field display precomputed di service."""
    id: int
    name: str
    color: str
    icon: str  # nama ikon Font Awesome tanpa prefix, mis. "briefcase"
    archived: bool
    created_at: datetime
    total_tasks: int
    active_tasks: int
    done_tasks: int


def _build_mock_projects() -> list[ProjectView]:
    now = datetime.now()
    all_tasks = task_service.get_all()
    specs = [
        (1, "Pekerjaan", "#3B82F6", "briefcase", False, now - timedelta(days=30)),
        (2, "Pribadi", "#10B981", "house", False, now - timedelta(days=25)),
        (3, "Belajar", "#14B8A6", "book-open", False, now - timedelta(days=14)),
        (4, "Ide & Riset", "#EC4899", "lightbulb", False, now - timedelta(days=7)),
    ]
    views = []
    for pid, name, color, icon, archived, created_at in specs:
        tasks = [t for t in all_tasks if t.project_id == pid]
        done = [t for t in tasks if t.status == "done"]
        views.append(ProjectView(
            id=pid,
            name=name,
            color=color,
            icon=icon,
            archived=archived,
            created_at=created_at,
            total_tasks=len(tasks),
            active_tasks=len(tasks) - len(done),
            done_tasks=len(done),
        ))
    return views


class ProjectService:
    """CRUD + aturan bisnis Project (mock, Phase 1)."""

    def get_all(self, include_archived: bool = False) -> list[ProjectView]:
        projects = _build_mock_projects()
        if not include_archived:
            return [p for p in projects if not p.archived]
        return projects

    def get_by_id(self, project_id: int) -> ProjectView | None:
        return next((p for p in _build_mock_projects() if p.id == project_id), None)

    # ── Aksi tulis: simulasi (view-first) ──
    def create(self, **data) -> None:
        """Simulasi — belum persist (Phase 2: insert ORM)."""

    def update(self, project_id: int, **data) -> None:
        """Simulasi — belum persist."""

    def set_archived(self, project_id: int, archived: bool) -> None:
        """Simulasi — belum persist."""

    def delete(self, project_id: int) -> None:
        """Simulasi — belum persist."""


project_service = ProjectService()
