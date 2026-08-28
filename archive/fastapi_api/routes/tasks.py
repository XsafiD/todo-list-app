"""Task CRUD routes."""
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import require_auth
from app.database import get_db
from app.models import Project, Reminder, ReminderType, Task, TaskStatus
from app.schemas import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter(dependencies=[Depends(require_auth)])


def _get_task_or_404(db: Session, task_id: int) -> Task:
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


def _sync_day_h_reminder(db: Session, task: Task) -> None:
    """Ensure a Day-H reminder exists for tasks with a deadline (and only then)."""
    day_h = db.scalars(
        select(Reminder).where(
            Reminder.task_id == task.id,
            Reminder.reminder_type == ReminderType.DAY_H,
        )
    ).first()

    if task.deadline and day_h is None:
        db.add(Reminder(task_id=task.id, reminder_type=ReminderType.DAY_H))
    elif task.deadline is None and day_h is not None and not day_h.sent:
        db.delete(day_h)


@router.get("/tasks", response_model=list[TaskResponse])
async def list_all_tasks(status_filter: str | None = None, project_id: int | None = None, db: Session = Depends(get_db)):
    stmt = select(Task)
    if status_filter:
        try:
            stmt = stmt.where(Task.status == TaskStatus(status_filter))
        except ValueError:
            raise HTTPException(422, f"Invalid status '{status_filter}'")
    if project_id is not None:
        stmt = stmt.where(Task.project_id == project_id)
    return db.scalars(stmt.order_by(Task.created_at.desc())).all()


@router.get("/projects/{project_id}/tasks", response_model=list[TaskResponse])
async def list_project_tasks(project_id: int, db: Session = Depends(get_db)):
    from app.models import Project
    project = db.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db.scalars(
        select(Task).where(Task.project_id == project_id).order_by(Task.created_at.desc(), Task.id.desc())
    ).all()


@router.post("/projects/{project_id}/tasks", response_model=TaskResponse, status_code=201)
async def create_task(project_id: int, payload: TaskCreate, db: Session = Depends(get_db)):
    project = db.get(Project, project_id)
    if project is None:
        raise HTTPException(404, "Project not found")
    task = Task(project_id=project_id, **payload.model_dump())
    db.add(task)
    db.flush()  # populate task.id
    _sync_day_h_reminder(db, task)
    db.commit()
    db.refresh(task)
    return task


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, db: Session = Depends(get_db)):
    return _get_task_or_404(db, task_id)


@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)):
    task = _get_task_or_404(db, task_id)
    data = payload.model_dump(exclude_unset=True)

    for field, value in data.items():
        setattr(task, field, value)

    # Keep completed_at consistent with status
    if task.status == TaskStatus.DONE and task.completed_at is None:
        task.completed_at = datetime.utcnow()
    elif task.status != TaskStatus.DONE and "status" in data:
        task.completed_at = None

    _sync_day_h_reminder(db, task)
    db.commit()
    db.refresh(task)
    return task


@router.patch("/tasks/{task_id}/complete", response_model=TaskResponse)
async def toggle_task_complete(task_id: int, db: Session = Depends(get_db)):
    """Toggle task completion status."""
    task = _get_task_or_404(db, task_id)
    if task.status == TaskStatus.DONE:
        task.status = TaskStatus.TODO
        task.completed_at = None
    else:
        task.status = TaskStatus.DONE
        task.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(task)
    return task


@router.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = _get_task_or_404(db, task_id)
    db.delete(task)
    db.commit()
