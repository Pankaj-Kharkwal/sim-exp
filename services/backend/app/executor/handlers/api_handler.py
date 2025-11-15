"""
API Block Handler
Handles HTTP/API request blocks
"""
import httpx
from typing import Any, Dict
from app.executor.types import (
    BlockHandler,
    BlockType,
    SerializedBlock,
    ExecutionContext,
    BlockResult,
)


class ApiBlockHandler:
    """Handler for API blocks that make external HTTP requests"""

    def can_handle(self, block: SerializedBlock) -> bool:
        """Check if this is an API block"""
        return block.metadata.get("id") == BlockType.API

    async def execute(
        self,
        ctx: ExecutionContext,
        block: SerializedBlock,
        inputs: Dict[str, Any],
    ) -> Any:
        """
        Execute an API request block

        Args:
            ctx: Execution context
            block: Block configuration
            inputs: Input values for the block

        Returns:
            API response data
        """
        # Extract request parameters
        url = inputs.get("url", "").strip()
        method = inputs.get("method", "GET").upper()
        headers = inputs.get("headers", {})
        params = inputs.get("params", {})
        body = inputs.get("body")

        # Validate URL
        if not url:
            return {"data": None, "status": 200, "headers": {}}

        # Remove quotes if present
        if url.startswith(('"', "'")) and url.endswith(('"', "'")):
            url = url[1:-1]

        # Validate URL format
        if not url.startswith(("http://", "https://")):
            raise ValueError(
                f'Invalid URL: "{url}" - URL must include protocol (try "https://{url}")'
            )

        # Process body if present
        if body is not None:
            if isinstance(body, str):
                body = body.strip()
                if body.startswith(("{", "[")):
                    import json

                    try:
                        body = json.loads(body)
                    except json.JSONDecodeError:
                        pass

        # Make HTTP request
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    params=params,
                    json=body if isinstance(body, (dict, list)) else None,
                    data=body if isinstance(body, str) else None,
                )

                # Parse response
                try:
                    data = response.json()
                except Exception:
                    data = response.text

                return {
                    "data": data,
                    "status": response.status_code,
                    "headers": dict(response.headers),
                    "statusText": response.reason_phrase,
                }

            except httpx.TimeoutException:
                raise Exception(f"Request timeout for {url}")
            except httpx.RequestError as e:
                raise Exception(f"Request failed: {str(e)}")
            except Exception as e:
                raise Exception(f"API request failed: {str(e)}")
