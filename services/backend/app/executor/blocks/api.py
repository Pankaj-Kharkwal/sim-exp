"""API block executor - HTTP requests"""

from typing import Any
import httpx

from app.core.logging import get_logger
from app.executor.state import WorkflowState

logger = get_logger(__name__)


async def execute_api_block(
    block: dict[str, Any], input_data: dict[str, Any], state: WorkflowState
) -> dict[str, Any]:
    """Execute an API HTTP request block"""

    logger.info("api_block_executing", block_id=block["id"], url=input_data.get("url"))

    # Extract configuration
    url = input_data.get("url")
    method = input_data.get("method", "GET").upper()
    headers = input_data.get("headers", {})
    body = input_data.get("body")
    timeout = input_data.get("timeout", 30.0)

    if not url:
        raise ValueError("URL is required for API block")

    # Make HTTP request
    async with httpx.AsyncClient() as client:
        request_kwargs = {
            "method": method,
            "url": url,
            "headers": headers,
            "timeout": timeout,
        }

        if body and method in ["POST", "PUT", "PATCH"]:
            request_kwargs["json"] = body

        response = await client.request(**request_kwargs)

    # Parse response
    try:
        response_data = response.json()
    except Exception:
        response_data = response.text

    logger.info(
        "api_block_completed",
        block_id=block["id"],
        status_code=response.status_code,
    )

    return {
        "status_code": response.status_code,
        "headers": dict(response.headers),
        "data": response_data,
        "success": 200 <= response.status_code < 300,
    }
