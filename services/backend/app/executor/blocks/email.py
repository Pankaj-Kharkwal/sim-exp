"""Email block executor - Send emails"""

from typing import Any, Optional
import httpx

from app.core.config import settings
from app.core.logging import get_logger
from app.executor.state import WorkflowState

logger = get_logger(__name__)


class EmailError(Exception):
    """Custom exception for email errors"""
    pass


async def execute_email_block(
    block: dict[str, Any], input_data: dict[str, Any], state: WorkflowState
) -> dict[str, Any]:
    """Execute an email sending block

    Uses Resend API for email delivery

    Supports:
    - HTML and plain text emails
    - Multiple recipients
    - CC and BCC
    - Attachments (future)
    - Custom reply-to
    """

    logger.info(
        "email_block_executing",
        block_id=block["id"],
        to=input_data.get("to"),
    )

    # Extract email configuration
    to = input_data.get("to")
    subject = input_data.get("subject")
    html = input_data.get("html")
    text = input_data.get("text")
    from_email = input_data.get("from", settings.FROM_EMAIL if hasattr(settings, 'FROM_EMAIL') else "noreply@pankh.ai")
    reply_to = input_data.get("reply_to")
    cc = input_data.get("cc", [])
    bcc = input_data.get("bcc", [])
    api_key = input_data.get("api_key") or (settings.RESEND_API_KEY if hasattr(settings, 'RESEND_API_KEY') else None)

    # Validation
    if not to:
        raise EmailError("Recipient email (to) is required")

    if not subject:
        raise EmailError("Email subject is required")

    if not html and not text:
        raise EmailError("Email body (html or text) is required")

    if not api_key:
        raise EmailError("Resend API key is required")

    # Prepare email payload
    email_payload = {
        "from": from_email,
        "to": [to] if isinstance(to, str) else to,
        "subject": subject,
    }

    if html:
        email_payload["html"] = html

    if text:
        email_payload["text"] = text

    if reply_to:
        email_payload["reply_to"] = reply_to

    if cc:
        email_payload["cc"] = [cc] if isinstance(cc, str) else cc

    if bcc:
        email_payload["bcc"] = [bcc] if isinstance(bcc, str) else bcc

    # Send email via Resend API
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.resend.com/emails",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json=email_payload,
                timeout=30.0,
            )

            response.raise_for_status()
            result = response.json()

            logger.info(
                "email_block_completed",
                block_id=block["id"],
                email_id=result.get("id"),
            )

            return {
                "success": True,
                "email_id": result.get("id"),
                "to": to,
                "subject": subject,
                "from": from_email,
            }

    except httpx.HTTPStatusError as e:
        logger.error(
            "email_send_failed",
            block_id=block["id"],
            status_code=e.response.status_code,
            error=e.response.text,
        )

        raise EmailError(f"Email send failed: {e.response.text}") from e

    except Exception as e:
        logger.error(
            "email_error",
            block_id=block["id"],
            error=str(e),
            exc_info=True,
        )

        raise EmailError(f"Email error: {str(e)}") from e
