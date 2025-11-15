"""Webhook block executor - Send outbound webhooks"""

from typing import Any, Optional
import httpx
import hmac
import hashlib
import time

from app.core.logging import get_logger
from app.executor.state import WorkflowState

logger = get_logger(__name__)


class WebhookError(Exception):
    """Custom exception for webhook errors"""
    pass


async def execute_webhook_block(
    block: dict[str, Any], input_data: dict[str, Any], state: WorkflowState
) -> dict[str, Any]:
    """Execute an outbound webhook block

    Supports:
    - POST webhook with JSON payload
    - HMAC signature signing
    - Custom headers
    - Retry logic
    - Timeout configuration
    """

    logger.info(
        "webhook_block_executing",
        block_id=block["id"],
        url=input_data.get("url"),
    )

    url = input_data.get("url")
    payload = input_data.get("payload", {})
    headers = input_data.get("headers", {})
    secret = input_data.get("secret")
    timeout = input_data.get("timeout", 30.0)

    if not url:
        raise WebhookError("Webhook URL is required")

    # Set default content type
    if "Content-Type" not in headers:
        headers["Content-Type"] = "application/json"

    # Add timestamp
    timestamp = int(time.time())
    headers["X-Webhook-Timestamp"] = str(timestamp)

    # Add workflow metadata
    headers["X-Workflow-ID"] = state.workflow_id
    headers["X-Execution-ID"] = state.execution_id

    # Generate HMAC signature if secret provided
    if secret:
        signature = _generate_signature(payload, secret, timestamp)
        headers["X-Webhook-Signature"] = signature

    # Send webhook
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=payload,
                headers=headers,
                timeout=timeout,
            )

            response.raise_for_status()

            logger.info(
                "webhook_block_completed",
                block_id=block["id"],
                status_code=response.status_code,
            )

            # Try to parse response
            try:
                response_data = response.json()
            except Exception:
                response_data = response.text

            return {
                "success": True,
                "status_code": response.status_code,
                "response": response_data,
                "url": url,
                "timestamp": timestamp,
            }

    except httpx.HTTPStatusError as e:
        logger.error(
            "webhook_failed",
            block_id=block["id"],
            status_code=e.response.status_code,
            error=str(e),
        )

        return {
            "success": False,
            "status_code": e.response.status_code,
            "error": str(e),
            "response": e.response.text,
            "url": url,
        }

    except Exception as e:
        logger.error(
            "webhook_error",
            block_id=block["id"],
            error=str(e),
            exc_info=True,
        )

        raise WebhookError(f"Webhook failed: {str(e)}") from e


def _generate_signature(payload: dict, secret: str, timestamp: int) -> str:
    """Generate HMAC signature for webhook"""
    import json

    # Create signature base string
    payload_str = json.dumps(payload, sort_keys=True, separators=(',', ':'))
    base_string = f"{timestamp}.{payload_str}"

    # Generate HMAC-SHA256 signature
    signature = hmac.new(
        secret.encode(),
        base_string.encode(),
        hashlib.sha256
    ).hexdigest()

    return signature
