"""Webhook configuration and notification management routes."""
import json
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, or_
from sqlalchemy.orm import Session

from app.api.dependencies import require_auth
from app.database import get_db
from app.models import NotificationLog, WebhookConfig
from app.schemas import WebhookConfigCreate, WebhookConfigResponse, NotificationLogResponse

router = APIRouter(dependencies=[Depends(require_auth)])


# ── Webhook Config ───────────────────────────────────────────────
@router.get("/webhook/config", response_model=list[WebhookConfigResponse])
async def list_webhook_configs(db: Session = Depends(get_db)):
    """List all webhook configurations."""
    return db.scalars(select(WebhookConfig)).all()


@router.post("/webhook/config", response_model=WebhookConfigResponse)
async def create_webhook_config(payload: WebhookConfigCreate, db: Session = Depends(get_db)):
    """Create/update webhook configuration."""
    # Check if active config exists
    existing_active = db.scalar(
        select(WebhookConfig).where(WebhookConfig.is_active.is_(True))
    )
    
    if existing_active:
        # Update existing (replace mode - single active config per system)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(existing_active, field, value)
        
        # Clear headers JSON if dict was provided
        if "headers" in payload.model_fields_set and isinstance(value := payload.headers, dict):
            existing_active.headers = json.dumps(value, indent=2)
        
        db.commit()
        db.refresh(existing_active)
        return existing_active
    else:
        # Create new
        config = WebhookConfig(
            name=payload.name,
            endpoint_url=payload.endpoint_url,
            message_template=payload.message_template,
        )
        
        if payload.headers:
            config.headers = json.dumps(payload.headers, indent=2)
        
        db.add(config)
        db.commit()
        db.refresh(config)
        return config


@router.get("/webhook/test")
async def test_notification(
    db: Session = Depends(get_db),
    test_phone: str = Query(default="+6281234567890", description="Test phone number"),
    test_message: Optional[str] = Query(default=None, description="Custom test message"),
):
    """Send test notification to configured webhook endpoint."""
    from app.services.webhook import send_webhook
    
    # Get active webhook config
    config = db.scalar(
        select(WebhookConfig).where(WebhookConfig.is_active.is_(True)).limit(1)
    )
    
    if not config:
        raise HTTPException(
            status_code=404, 
            detail="No active webhook configuration found"
        )

    # Prepare message
    message = test_message or (
        f"🧪 Test Notification\n"
        f"From: Dashboardku\n"
        f"Endpoint: {config.endpoint_url}\n"
        f"This is a test notification."
    )

    # Parse headers
    headers = {}
    if config.headers:
        try:
            headers = json.loads(config.headers)
        except:
            pass

    try:
        # Send test notification
        result = await send_webhook(
            message=message,
            context={"test": True},
            headers=headers,
            endpoint_url=config.endpoint_url,
        )

        return {
            "status": "success",
            "message": "Test notification sent",
            "response": result,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send test notification: {str(e)}"
        )


# ── Notification Logs ─────────────────────────────────────────────
@router.get("/notifications/logs", response_model=list[NotificationLogResponse])
async def get_notification_logs(
    limit: int = Query(50, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    status_filter: Optional[str] = Query(None, regex="^(sent|failed|pending)$"),
    task_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    """Get notification delivery logs."""
    stmt = select(NotificationLog).order_by(NotificationLog.created_at.desc())

    if status_filter:
        stmt = stmt.where(NotificationLog.status == status_filter)
    
    if task_id is not None:
        stmt = stmt.where(NotificationLog.task_id == task_id)

    stmt = stmt.offset(offset).limit(limit)
    return db.scalars(stmt).all()
