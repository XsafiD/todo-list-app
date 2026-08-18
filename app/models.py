"""SQLAlchemy ORM models for Dashboardku."""
from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class ReminderType(str, Enum):
    DAY_H = "day_h"
    RELATIVE = "relative"
    ABSOLUTE = "absolute"


class ReminderUnit(str, Enum):
    MINUTES = "minutes"
    HOURS = "hours"
    DAYS = "days"


class NotificationStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"


class Project(Base):
    __tablename__ = "projects"
    __table_args__ = (Index("idx_projects_name", "name"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    color: Mapped[str] = mapped_column(String(7), default="#3B82F6", nullable=False)
    icon: Mapped[str | None] = mapped_column(String(50), nullable=True)
    archived: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    tasks: Mapped[list[Task]] = relationship(back_populates="project", lazy="selectin")


class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = (
        Index("idx_tasks_project_id", "project_id"),
        Index("idx_tasks_deadline", "deadline"),
        Index("idx_tasks_status", "status"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("projects.id", ondelete="SET NULL"), nullable=True
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    priority: Mapped[TaskPriority] = mapped_column(
        SQLEnum(TaskPriority, name="task_priority"), default=TaskPriority.MEDIUM, nullable=False
    )
    status: Mapped[TaskStatus] = mapped_column(
        SQLEnum(TaskStatus, name="task_status"), default=TaskStatus.TODO, nullable=False
    )
    deadline: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    project: Mapped[Project | None] = relationship(back_populates="tasks")
    reminders: Mapped[list[Reminder]] = relationship(back_populates="task", cascade="all, delete-orphan", lazy="selectin")


class Reminder(Base):
    __tablename__ = "reminders"
    __table_args__ = (Index("idx_reminders_task_id", "task_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    reminder_type: Mapped[ReminderType] = mapped_column(SQLEnum(ReminderType, name="reminder_type"), nullable=False)
    relative_value: Mapped[int | None] = mapped_column(Integer, nullable=True)
    relative_unit: Mapped[ReminderUnit | None] = mapped_column(SQLEnum(ReminderUnit, name="reminder_unit"), nullable=True)
    absolute_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    sent: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    task: Mapped[Task] = relationship(back_populates="reminders")


class WebhookConfig(Base):
    __tablename__ = "webhook_configs"
    __table_args__ = (Index("idx_webhook_config_active", "is_active"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    endpoint_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    headers: Mapped[str | None] = mapped_column(Text, nullable=True)
    message_template: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, onupdate=func.now(), nullable=True)


class NotificationLog(Base):
    __tablename__ = "notification_logs"
    __table_args__ = (
        Index("idx_notification_log_task_id", "task_id"),
        Index("idx_notification_log_reminder_id", "reminder_id"),
        Index("idx_notification_log_webhook_id", "webhook_config_id"),
        Index("idx_notification_log_status", "status"),
        Index("idx_notification_log_created", "created_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    task_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True)
    reminder_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("reminders.id", ondelete="SET NULL"), nullable=True)
    webhook_config_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("webhook_configs.id", ondelete="SET NULL"), nullable=True)
    status: Mapped[NotificationStatus] = mapped_column(SQLEnum(NotificationStatus, name="notification_status"), default=NotificationStatus.PENDING, nullable=False)
    response_code: Mapped[int | None] = mapped_column(Integer, nullable=True)
    response_body: Mapped[str | None] = mapped_column(Text, nullable=True)
    retry_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
