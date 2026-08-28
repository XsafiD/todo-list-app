"""Pydantic request/response schemas."""
from datetime import datetime
from typing import Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, model_validator

Priority = Literal["low", "medium", "high"]
TaskStatusLiteral = Literal["todo", "in_progress", "done"]
ReminderTypeLiteral = Literal["day_h", "relative", "absolute"]
ReminderUnitLiteral = Literal["minutes", "hours", "days"]

# For handling SQLAlchemy enums + strings
PriorityStr = Union[str, Literal["low", "medium", "high"]]
StatusStr = Union[str, Literal["todo", "in_progress", "done"]]


# ── Projects ───────────────────────────────────────────────
class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    color: str = Field(default="#3B82F6", pattern=r"^#[0-9A-Fa-f]{6}$")
    icon: Optional[str] = Field(default=None, max_length=50)


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    color: Optional[str] = Field(default=None, pattern=r"^#[0-9A-Fa-f]{6}$")
    icon: Optional[str] = Field(default=None, max_length=50)


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    color: str
    icon: Optional[str] = None
    archived: bool = False
    created_at: datetime


# ── Tasks ───────────────────────────────────────────────────
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    priority: PriorityStr = "medium"  # Accepts both string and str-enum
    status: StatusStr = "todo"
    deadline: Optional[datetime] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=500)
    description: Optional[str] = None
    priority: Optional[PriorityStr] = None
    status: Optional[StatusStr] = None
    deadline: Optional[datetime] = None


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    priority: str  # Will be coerced by str() since str-Enum
    status: str
    deadline: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime


# ── Reminders ───────────────────────────────────────────────
class ReminderCreate(BaseModel):
    reminder_type: ReminderTypeLiteral
    relative_value: Optional[int] = Field(default=None, gt=0)
    relative_unit: Optional[ReminderUnitLiteral] = None
    absolute_time: Optional[datetime] = None

    @model_validator(mode="after")
    def validate_config(self) -> "ReminderCreate":
        if self.reminder_type == "relative":
            if self.relative_value is None or self.relative_unit is None:
                raise ValueError("Relative reminders require relative_value and relative_unit")
        elif self.reminder_type == "absolute":
            if self.absolute_time is None:
                raise ValueError("Absolute reminders require absolute_time")
        return self


class ReminderUpdate(BaseModel):
    relative_value: Optional[int] = Field(default=None, gt=0)
    relative_unit: Optional[ReminderUnitLiteral] = None
    absolute_time: Optional[datetime] = None


class ReminderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_id: int
    reminder_type: str
    relative_value: Optional[int] = None
    relative_unit: Optional[str] = None
    absolute_time: Optional[datetime] = None
    sent: bool = False
    sent_at: Optional[datetime] = None


# ── Auth ────────────────────────────────────────────────────
class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    username: str


# ── Stats ───────────────────────────────────────────────────
class StatsResponse(BaseModel):
    total_tasks: int = 0
    active_tasks: int = 0
    completed_tasks: int = 0
    overdue_tasks: int = 0
    total_projects: int = 0
    active_projects: int = 0


# ── Webhook Config ───────────────────────────────────────────────
class WebhookConfigCreate(BaseModel):
    name: Optional[str] = None
    endpoint_url: str
    headers: Optional[dict] = None
    message_template: Optional[str] = None


class WebhookConfigResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: Optional[str] = None
    endpoint_url: str
    headers: Optional[str] = None
    message_template: Optional[str] = None
    is_active: bool = True
    created_at: datetime


# ── Notification Logs ────────────────────────────────────────────
class NotificationLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_id: Optional[int] = None
    reminder_id: Optional[int] = None
    webhook_config_id: Optional[int] = None
    status: str
    response_code: Optional[int] = None
    response_body: Optional[str] = None
    retry_count: int = 0
    created_at: datetime
