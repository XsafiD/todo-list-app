"""Webhook notification service for sending to WAHA and other endpoints."""
import asyncio
import json
from typing import Any, Dict, Optional

import httpx


class WebhookSender:
    """Service for sending notifications via webhooks."""

    def __init__(self, base_url: str = "", timeout: float = 30.0):
        self.base_url = base_url
        self.timeout = timeout

    async def send_webhook(
        self, 
        message: str, 
        context: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        endpoint_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Send notification via webhook (WAHA or custom endpoint)."""
        
        url = endpoint_url or self.base_url
        
        if not url:
            raise ValueError("No webhook URL configured")
        
        # Prepare request payload
        payload = {"message": message}
        if context:
            payload.update(context)

        # Set default headers
        request_headers = {
            "Content-Type": "application/json",
            **{k: v for k, v in (headers or {}).items()}
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(url, json=payload, headers=request_headers)
            
            # Raise exception for HTTP errors
            response.raise_for_status()
            
            # Parse JSON response if possible
            try:
                return response.json()
            except:
                return {"raw_response": response.text, "status_code": response.status_code}

    async def send_to_waha(self, phone_number: str, message: str) -> Dict[str, Any]:
        """Convenience method for WAHA webhook format."""
        # WAHA typically expects: /sendText/{phone}/{message}
        # Or POST body: {"chatId": "+62xxx", "text": "message"}
        payload = {
            "chatId": phone_number,
            "text": message
        }
        
        return await self.send_webhook(message, payload)

    async def retry_notification(
        self,
        message: str,
        context: Dict[str, Any],
        max_retries: int = 3,
        backoff_multiplier: float = 2.0,
        initial_delay: float = 1.0,
        **kwargs
    ) -> bool:
        """Retry failed notification with exponential backoff."""
        
        last_error = None
        
        for attempt in range(max_retries):
            try:
                await self.send_webhook(message, context, **kwargs)
                print(f"[Webhook] Success on attempt {attempt + 1}")
                return True
                
            except Exception as e:
                last_error = e
                delay = initial_delay * (backoff_multiplier ** attempt)
                
                if attempt < max_retries - 1:
                    print(f"[Webhook] Failed (attempt {attempt + 1}), retrying in {delay:.1f}s")
                    await asyncio.sleep(delay)

        print(f"[Webhook] All retries failed: {last_error}")
        return False

    def validate_url(self, url: str) -> bool:
        """Validate webhook URL format."""
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)


# Create singleton instance
webhook_sender = WebhookSender()


async def send_notification_via_waha(phone: str, message: str) -> Dict[str, Any]:
    """Send WhatsApp message via WAHA gateway."""
    if not hasattr(sender, "waha_base_url"):
        raise ValueError("WAHA_WEBHOOK_URL not configured")
    
    return await sender.send_to_waha(phone, message)


async def send_webhook(message: str, context: dict = None, **kwargs):
    """Convenience function for sending webhooks."""
    return await webhook_sender.send_webhook(message, context or {}, **kwargs)
