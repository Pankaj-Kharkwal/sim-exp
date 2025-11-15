"""HTTP block executor - Make HTTP requests"""

from typing import Any, Optional
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.logging import get_logger
from app.executor.state import WorkflowState

logger = get_logger(__name__)


class HTTPBlockError(Exception):
    """Custom exception for HTTP block errors"""

    pass


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    reraise=True,
)
async def _make_request_with_retry(
    client: httpx.AsyncClient,
    method: str,
    url: str,
    **kwargs,
) -> httpx.Response:
    """Make HTTP request with retry logic"""
    response = await client.request(method, url, **kwargs)
    response.raise_for_status()
    return response


async def execute_http_block(
    block: dict[str, Any], input_data: dict[str, Any], state: WorkflowState
) -> dict[str, Any]:
    """Execute an HTTP request block

    Supports:
    - GET, POST, PUT, PATCH, DELETE methods
    - Headers, query parameters, body
    - Authentication (Bearer, Basic, API Key)
    - Retry logic with exponential backoff
    - Timeout configuration
    """

    logger.info(
        "http_block_executing",
        block_id=block["id"],
        method=input_data.get("method", "GET"),
        url=input_data.get("url"),
    )

    # Extract configuration
    method = input_data.get("method", "GET").upper()
    url = input_data.get("url")
    headers = input_data.get("headers", {})
    params = input_data.get("params", {})
    body = input_data.get("body")
    timeout = input_data.get("timeout", 30.0)
    follow_redirects = input_data.get("follow_redirects", True)
    verify_ssl = input_data.get("verify_ssl", True)

    # Authentication
    auth_type = input_data.get("auth_type")  # bearer, basic, api_key
    auth_token = input_data.get("auth_token")
    auth_username = input_data.get("auth_username")
    auth_password = input_data.get("auth_password")
    api_key_header = input_data.get("api_key_header", "X-API-Key")

    # Validation
    if not url:
        raise HTTPBlockError("URL is required for HTTP block")

    if method not in ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]:
        raise HTTPBlockError(f"Unsupported HTTP method: {method}")

    # Setup authentication
    if auth_type == "bearer" and auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"
    elif auth_type == "api_key" and auth_token:
        headers[api_key_header] = auth_token

    # Basic auth is handled separately
    auth = None
    if auth_type == "basic" and auth_username and auth_password:
        auth = httpx.BasicAuth(auth_username, auth_password)

    # Prepare request kwargs
    request_kwargs: dict[str, Any] = {
        "headers": headers,
        "params": params,
        "timeout": timeout,
        "follow_redirects": follow_redirects,
    }

    if not verify_ssl:
        request_kwargs["verify"] = False

    if auth:
        request_kwargs["auth"] = auth

    # Add body for methods that support it
    if method in ["POST", "PUT", "PATCH"] and body is not None:
        # Determine content type
        content_type = headers.get("Content-Type", "application/json")

        if "application/json" in content_type:
            request_kwargs["json"] = body
        elif "application/x-www-form-urlencoded" in content_type:
            request_kwargs["data"] = body
        else:
            request_kwargs["content"] = body if isinstance(body, (str, bytes)) else str(body)

    # Make the request
    try:
        async with httpx.AsyncClient() as client:
            response = await _make_request_with_retry(client, method, url, **request_kwargs)

        # Parse response
        response_headers = dict(response.headers)
        status_code = response.status_code

        # Try to parse as JSON
        try:
            response_data = response.json()
        except Exception:
            response_data = response.text

        logger.info(
            "http_block_completed",
            block_id=block["id"],
            status_code=status_code,
            response_size=len(response.text),
        )

        return {
            "status_code": status_code,
            "headers": response_headers,
            "data": response_data,
            "text": response.text,
            "ok": 200 <= status_code < 300,
            "url": str(response.url),
        }

    except httpx.HTTPStatusError as e:
        logger.error(
            "http_block_failed",
            block_id=block["id"],
            error=str(e),
            status_code=e.response.status_code,
        )

        # Return error response
        return {
            "status_code": e.response.status_code,
            "headers": dict(e.response.headers),
            "data": e.response.text,
            "text": e.response.text,
            "ok": False,
            "error": str(e),
            "url": str(e.response.url),
        }

    except httpx.RequestError as e:
        logger.error(
            "http_block_request_failed",
            block_id=block["id"],
            error=str(e),
            exc_info=True,
        )

        raise HTTPBlockError(f"HTTP request failed: {str(e)}") from e

    except Exception as e:
        logger.error(
            "http_block_unexpected_error",
            block_id=block["id"],
            error=str(e),
            exc_info=True,
        )

        raise HTTPBlockError(f"Unexpected error in HTTP block: {str(e)}") from e
