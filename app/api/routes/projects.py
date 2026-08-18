"""Project CRUD routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import update
from sqlalchemy.orm import Session

from app.api.dependencies import require_auth
from app.database import get_db
from app.models import Project, Task
from app.schemas import ProjectCreate, ProjectResponse, ProjectUpdate

router = APIRouter(dependencies=[Depends(require_auth)])


def _get_project_or_404(db: Session, project_id: int) -> Project:
    project = db.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.get("/projects", response_model=list[ProjectResponse])
async def list_projects(include_archived: bool = False, db: Session = Depends(get_db)):
    from sqlalchemy import select
    stmt = select(Project)
    if not include_archived:
        stmt = stmt.where(Project.archived.is_(False))
    return db.scalars(stmt.order_by(Project.created_at.desc(), Project.id.desc())).all()


@router.post("/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    project = Project(**payload.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int, db: Session = Depends(get_db)):
    return _get_project_or_404(db, project_id)


@router.put("/projects/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: int, payload: ProjectUpdate, db: Session = Depends(get_db)):
    project = _get_project_or_404(db, project_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(project, field, value)
    db.commit()
    db.refresh(project)
    return project


@router.patch("/projects/{project_id}/archive", response_model=ProjectResponse)
async def archive_project(project_id: int, archived: bool = True, db: Session = Depends(get_db)):
    """Archive (soft delete) a project. Use ?archived=false to unarchive."""
    project = _get_project_or_404(db, project_id)
    project.archived = archived
    db.commit()
    db.refresh(project)
    return project


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = _get_project_or_404(db, project_id)
    # Keep tasks as unassigned instead of deleting them
    db.execute(update(Task).where(Task.project_id == project_id).values(project_id=None))
    db.delete(project)
    db.commit()
