"""Notification template and logging services."""
import json
from datetime import datetime
from typing import Optional


def render_notification_template(
    task_title: str,
    project_name: str,
    deadline: datetime,
    template: Optional[str] = None,
) -> str:
    """Render notification message with context variables.
    
    Variables available in template:
        {task_title} - Task title/name
        {project_name} - Project name or "Unknown"
        {deadline} - Deadline formatted as YYYY-MM-DD HH:MM
        {priority} - Task priority (low/medium/high)
        {status} - Task status (todo/in_progress/done)
        {reminder_type} - Type of reminder that triggered
    
    If no template provided, uses default format:
        🔔 Reminder: {task_title}
        📁 Project: {project_name}
        ⏰ Deadline: {deadline}
    """
    
    if not template:
        # Default template
        return (
            f"🔔 Reminder: {task_title}\n"
            f"📁 Project: {project_name}\n"
            f"⏰ Deadline: {deadline.strftime('%Y-%m-%d %H:%M')}"
        )
    
    # Parse template and replace variables
    result = template
    result = result.replace("{task_title}", task_title)
    result = result.replace("{project_name}", project_name)
    result = result.replace(
        "{deadline}", 
        deadline.strftime('%Y-%m-%d %H:%M')
    )
    result = result.replace("{priority}", "medium")  # Would need task object for real value
    result = result.replace("{status}", "todo")       # Would need task object for real value
    result = result.replace("{reminder_type}", "day_h")  # Would need reminder object for real value
    
    return result


async def save_notification_log(
    db_session,
    task_id: int,
    reminder_id: int,
    webhook_config_id: Optional[int],
    status: str,
    response_code: Optional[int],
    response_body: Optional[str],
):
    """Save notification log entry to database.
    
    This function is now handled in scheduler.py directly for better transaction control.
    Kept here for reference/compatibility.
    """
    from app.models import NotificationLog, NotificationStatus
    
    # Map string status to enum
    status_map = {
        "sent": NotificationStatus.SENT,
        "failed": NotificationStatus.FAILED,
        "pending": NotificationStatus.PENDING,
    }
    
    log_entry = NotificationLog(
        task_id=task_id,
        reminder_id=reminder_id,
        webhook_config_id=webhook_config_id,
        status=status_map.get(status.lower(), NotificationStatus.PENDING),
        response_code=response_code,
        response_body=response_body,
    )
    db_session.add(log_entry)
    db_session.flush()


def parse_webhook_headers(headers_json: Optional[str]) -> dict:
    """Parse JSON headers string from database field."""
    if not headers_json:
        return {}
    
    try:
        return json.loads(headers_json)
    except json.JSONDecodeError as e:
        print(f"Invalid webhook headers JSON: {e}")
        return {}


def get_current_timestamp_str() -> str:
    """Return current UTC timestamp in ISO format."""
    return datetime.utcnow().isoformat()
