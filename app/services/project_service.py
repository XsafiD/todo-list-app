"""ProjectService — business logic Project (ORM, Phase 2).

Kontrak return: DTO `ProjectView` untuk tampilan (counts precomputed via
aggregate query — 17-performance.md #1/#3), objek `Project` untuk operasi
tulis. Error kontrak: validasi gagal → `raise ValueError(pesan)`.
"""
import re
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import case, func, select, update

from app.extensions import db
from app.models import Project, Task, TaskStatus

HEX_COLOR_PATTERN = re.compile(r"^#[0-9A-Fa-f]{6}$")  # didefinisikan sekali (03-service.md #3)

_DEFAULT_ICON = "folder"


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
    archived_tasks: int


def _to_view(project: Project, total: int, active: int, archived_tasks: int) -> ProjectView:
    icon = (project.icon or "").strip().removeprefix("fa-") or _DEFAULT_ICON
    return ProjectView(
        id=project.id,
        name=project.name,
        color=project.color,
        icon=icon,
        archived=bool(project.archived),
        created_at=project.created_at,
        total_tasks=total,
        active_tasks=active,
        # done = selesai belum diarsip; archived ⊆ done → total = active + done + archived
        done_tasks=total - active - archived_tasks,
        archived_tasks=archived_tasks,
    )


def _counts_stmt():
    """Query aggregate project + jumlah task (1 query untuk semua project — anti N+1).

    Kolom: (Project, total, active, archived) — archived = task terarsip
    (subset dari done; invariant state machine: terarsip selalu done).
    """
    return (
        select(
            Project,
            func.count(Task.id).label("total"),
            func.coalesce(
                func.sum(case((Task.status != TaskStatus.DONE, 1), else_=0)), 0
            ).label("active"),
            func.coalesce(
                func.sum(case((Task.archived_at.is_not(None), 1), else_=0)), 0
            ).label("archived"),
        )
        .outerjoin(Task, Task.project_id == Project.id)
        .group_by(Project.id)
        .order_by(Project.created_at.desc(), Project.id.desc())
    )


class ProjectService:
    """CRUD + aturan bisnis Project."""

    # ── Read ──
    def get_all(self, include_archived: bool = False) -> list[ProjectView]:
        stmt = _counts_stmt()
        if not include_archived:
            stmt = stmt.where(Project.archived.is_(False))
        return [_to_view(p, total, int(active), int(archived)) for p, total, active, archived in db.session.execute(stmt)]

    def get_by_id(self, project_id: int) -> ProjectView | None:
        stmt = _counts_stmt().where(Project.id == project_id)
        row = db.session.execute(stmt).first()
        if row is None:
            return None
        project, total, active, archived = row
        return _to_view(project, total, int(active), int(archived))

    def count_all(self) -> tuple[int, int]:
        """Return (total_project, project_aktif) dalam satu query."""
        row = db.session.execute(
            select(func.count(Project.id), func.sum(case((Project.archived.is_(False), 1), else_=0)))
        ).one()
        return row[0] or 0, int(row[1] or 0)

    # ── Validasi (multi-layer: border form + sini — 16-security.md #4) ──
    def _validate(self, name: str, color: str) -> None:
        if not name or not name.strip():
            raise ValueError("Nama project wajib diisi.")
        if len(name.strip()) > 255:
            raise ValueError("Nama project maksimal 255 karakter.")
        if not HEX_COLOR_PATTERN.match(color or ""):
            raise ValueError("Warna harus format hex, mis. #3B82F6.")

    # ── Write ──
    def create(self, name: str, color: str, icon: str | None = None) -> Project:
        self._validate(name, color)
        project = Project(
            name=name.strip(),
            color=color,
            icon=(icon or "").strip().removeprefix("fa-") or None,
        )
        db.session.add(project)
        db.session.commit()
        return project

    def update(self, project_id: int, name: str, color: str, icon: str | None = None) -> Project:
        project = db.session.get(Project, project_id)
        if project is None:
            raise ValueError("Project tidak ditemukan.")
        self._validate(name, color)
        project.name = name.strip()
        project.color = color
        project.icon = (icon or "").strip().removeprefix("fa-") or None
        db.session.commit()
        return project

    def set_archived(self, project_id: int, archived: bool) -> Project:
        project = db.session.get(Project, project_id)
        if project is None:
            raise ValueError("Project tidak ditemukan.")
        project.archived = bool(archived)
        db.session.commit()
        return project

    def delete(self, project_id: int) -> Project:
        """Hapus project; task di dalamnya dilepas (project_id = NULL), tidak ikut terhapus."""
        project = db.session.get(Project, project_id)
        if project is None:
            raise ValueError("Project tidak ditemukan.")
        db.session.execute(
            update(Task).where(Task.project_id == project_id).values(project_id=None)
        )
        db.session.delete(project)
        db.session.commit()
        return project


project_service = ProjectService()
