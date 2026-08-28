"""Background job scheduler using APScheduler."""
import asyncio
from datetime import datetime
from typing import Any, Optional

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.config import settings
from app.database import get_db
from app.models import (
    NotificationLog, 
    Reminder, 
    Task, 
    TaskStatus, 
    WebhookConfig, 
    NotificationStatus
)
from app.services.notification import render_notification_template
from app.services.webhook import send_webhook


class SchedulerService:
    """Main scheduler service for deadline notifications."""

    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self._initialized = False

    def init(self) -> None:
        """Initialize scheduler if not already done."""
        if self._initialized:
            return
        
        # Run deadline checker every minute
        self.scheduler.add_job(
            check_and_notify_deadlines,
            trigger=CronTrigger(minute="*", hour="*"),
            id="check_deadlines",
            name="Check task deadlines",
            replace_existing=True,
        )

        # Start scheduler
        self.scheduler.start()
        self._initialized = True
        print("🕐 Scheduler initialized - running every minute")

    async def shutdown(self) -> None:
        """Gracefully stop the scheduler."""
        if self.scheduler.running:
            self.scheduler.shutdown(wait=False)
        print("🛑 Scheduler stopped")


async def check_and_notify_deadlines():
    """Job: Check all tasks and send notifications for approaching/dead deadlines."""
    print("\n[Scheduler] Checking deadlines...")

    db_session = None
    try:
        db_session = next(get_db())
        
        # Fetch all incomplete tasks with reminders that haven't been sent
        stmt = (
            select(Task)
            .where(Task.status != TaskStatus.DONE)
            .options(selectinload(Task.reminders))
        )
        tasks = db_session.scalars(stmt).all()

        now = datetime.utcnow()

        for task in tasks:
            for reminder in task.reminders:
                if reminder.sent:
                    continue
                
                should_notify = check_reminder_due(reminder, task.deadline, now)
                
                if should_notify:
                    await process_reminder(db_session, task, reminder)

        db_session.commit()
    except Exception as e:
        print(f"[Scheduler] Error during check: {e}")
    finally:
        if db_session:
            try:
                db_session.close()
            except:
                pass


def check_reminder_due(reminder: Reminder, task_deadline: Optional[datetime], now: datetime) -> bool:
    """Determine if a reminder should be triggered based on its type."""
    
    if reminder.reminder_type == "day_h":
        # Day-H reminder: trigger on the same day as deadline
        if task_deadline is None:
            return False
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        deadline_day = task_deadline.replace(hour=0, minute=0, second=0, microsecond=0)
        return deadline_day == today_start

    elif reminder.reminder_type == "relative":
        # Relative reminder: X units before deadline
        if task_deadline is None or reminder.relative_value is None or reminder.relative_unit is None:
            return False

        delta_seconds = calculate_relative_delta(
            reminder.relative_value, 
            reminder.relative_unit,
            task_deadline
        )

        threshold_time = task_deadline.replace(tzinfo=None) - delta_seconds
        return now >= threshold_time

    elif reminder.reminder_type == "absolute":
        # Absolute reminder: specific time
        if reminder.absolute_time is None:
            return False
        absolute_dt = reminder.absolute_time.replace(tzinfo=None)
        return now >= absolute_dt

    return False


def calculate_relative_delta(value: int, unit: str, task_deadline: datetime) -> int:
    """Calculate seconds offset for relative reminder."""
    from datetime import timedelta
    
    if unit == "minutes":
        return timedelta(minutes=value).total_seconds()
    elif unit == "hours":
        return timedelta(hours=value).total_seconds()
    elif unit == "days":
        return timedelta(days=value).total_seconds()
    
    return 0


async def process_reminder(db_session: Session, task: Task, reminder: Reminder) -> None:
    """Process a single reminder: send notification and log result."""
    print(f"[Notification] Processing reminder #{reminder.id} for task '{task.title}'")

    try:
        # Update reminder status
        reminder.sent = True
        reminder.sent_at = datetime.utcnow()
        db_session.flush()

        # Get webhook config
        webhook_config = db_session.scalar(
            select(WebhookConfig)
            .where(WebhookConfig.is_active.is_(True))
            .limit(1)
        )

        # Render message template
        project_name = task.project.name if task.project else "Unknown"
        template = webhook_config.message_template if webhook_config else None
        
        message = render_notification_template(
            task_title=task.title,
            project_name=project_name,
            deadline=task.deadline or datetime.utcnow(),
            template=template
        )

        response_code = None
        response_body = None

        # Send via webhook if configured
        if webhook_config:
            headers = {}
            if webhook_config.headers:
                try:
                    import json
                    headers = json.loads(webhook_config.headers)
                except:
                    pass

            try:
                result = await send_webhook(message, {"context": {
                    "task_id": task.id,
                    "project_id": task.project_id if task.project else None,
                    "reminder_id": reminder.id,
                }})
                response_code = 200
                response_body = str(result)
            except Exception as e:
                response_code = 500
                response_body = str(e)

        # Save notification log
        notification_log = NotificationLog(
            task_id=task.id,
            reminder_id=reminder.id,
            webhook_config_id=webhook_config.id if webhook_config else None,
            status=NotificationStatus.SENT if response_code == 200 else NotificationStatus.FAILED,
            response_code=response_code,
            response_body=response_body,
        )
        db_session.add(notification_log)

    except Exception as e:
        print(f"[Notification] Error processing reminder #{reminder.id}: {e}")
        # Log failure
        notification_log = NotificationLog(
            task_id=task.id,
            reminder_id=reminder.id,
            webhook_config_id=None,
            status=NotificationStatus.FAILED,
            response_code=500,
            response_body=str(e),
        )
        db_session.add(notification_log)

    db_session.flush()


# Create singleton instance
scheduler_service = SchedulerService()
