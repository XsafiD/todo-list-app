"""Reminder CRUD routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import require_auth
from app.database import get_db
from app.models import Reminder, ReminderType, Task
from app.schemas import ReminderCreate, ReminderResponse, ReminderUpdate

router = APIRouter(dependencies=[Depends(require_auth)])


def _get_reminder_or_404(db: Session, reminder_id: int) -> Reminder:
    reminder = db.get(Reminder, reminder_id)
    if reminder is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reminder not found")
    return reminder


def _validate_reminder_config(reminder: Reminder) -> None:
    """Validate reminder configuration based on type."""
    if reminder.reminder_type == ReminderType.RELATIVE:
        if reminder.relative_value is None or reminder.relative_unit is None:
            raise HTTPException(422, "Relative reminders require relative_value and relative_unit")
    elif reminder.reminder_type == ReminderType.ABSOLUTE:
        if reminder.absolute_time is None:
            raise HTTPException(422, "Absolute reminders require absolute_time")


@router.get("/tasks/{task_id}/reminders", response_model=list[ReminderResponse])
async def list_reminders(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db.scalars(select(Reminder).where(Reminder.task_id == task_id).order_by(Reminder.id)).all()


@router.post("/tasks/{task_id}/reminders", response_model=ReminderResponse, status_code=201)
async def create_reminder(task_id: int, payload: ReminderCreate, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    # Prevent duplicate Day-H reminders
    if payload.reminder_type == "day_h":
        existing = db.scalars(
            select(Reminder).where(
                Reminder.task_id == task_id,
                Reminder.reminder_type == ReminderType.DAY_H,
            )
        ).first()
        if existing is not None:
            raise HTTPException(409, "A Day-H reminder already exists for this task")

    reminder = Reminder(task_id=task_id, **payload.model_dump())
    _validate_reminder_config(reminder)
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder


@router.put("/reminders/{reminder_id}", response_model=ReminderResponse)
async def update_reminder(reminder_id: int, payload: ReminderUpdate, db: Session = Depends(get_db)):
    reminder = _get_reminder_or_404(db, reminder_id)
    if reminder.sent:
        raise HTTPException(409, "A sent reminder cannot be modified")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(reminder, field, value)
    _validate_reminder_config(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder


@router.delete("/reminders/{reminder_id}", status_code=204)
async def delete_reminder(reminder_id: int, db: Session = Depends(get_db)):
    reminder = _get_reminder_or_404(db, reminder_id)
    if reminder.sent:
        raise HTTPException(409, "A sent reminder cannot be deleted")
    db.delete(reminder)
    db.commit()
