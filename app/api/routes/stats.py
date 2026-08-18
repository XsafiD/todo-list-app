"""Dashboard statistics routes."""
from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.dependencies import require_auth
from app.database import get_db
from app.models import Project, Task, TaskStatus
from app.schemas import StatsResponse

router = APIRouter(dependencies=[Depends(require_auth)])


@router.get("/stats", response_model=StatsResponse)
async def get_stats(db: Session = Depends(get_db)):
    now = datetime.utcnow()
    total = db.scalar(select(func.count()).select_from(Task)) or 0
    completed = db.scalar(select(func.count()).select_from(Task).where(Task.status == TaskStatus.DONE)) or 0
    active = db.scalar(select(func.count()).select_from(Task).where(Task.status != TaskStatus.DONE)) or 0
    overdue = db.scalar(select(func.count()).select_from(Task).where(Task.deadline < now, Task.status != TaskStatus.DONE)) or 0
    total_projects = db.scalar(select(func.count()).select_from(Project)) or 0
    active_projects = db.scalar(select(func.count()).select_from(Project).where(Project.archived.is_(False))) or 0
    return StatsResponse(
        total_tasks=total,
        active_tasks=active,
        completed_tasks=completed,
        overdue_tasks=overdue,
        total_projects=total_projects,
        active_projects=active_projects,
    )
