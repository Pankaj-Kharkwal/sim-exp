"""Anthropic (Claude) block executor - AI model interactions"""

from typing import Any, Optional
import os
from anthropic import AsyncAnthropic

from app.core.logging import get_logger
from app.core.config import settings
from app.executor.state import WorkflowState

logger = get_logger(__name__)


async def execute_anthropic_block(
    block: dict[str, Any], input_data: dict[str, Any], state: WorkflowState
) -> dict[str, Any]:
    """
    Execute an Anthropic (Claude) block for AI interactions

    Supports:
    - Chat/text completions with Claude models
    - Streaming responses
    - Tool use / function calling
    - Vision (image analysis)
    """

    logger.info("anthropic_block_executing", block_id=block["id"])

    # Initialize Anthropic client
    api_key = input_data.get("api_key") or settings.ANTHROPIC_API_KEY or os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("Anthropic API key is required. Set ANTHROPIC_API_KEY environment variable or provide in block config.")

    client = AsyncAnthropic(api_key=api_key)

    try:
        result = await _execute_message_completion(client, input_data)

        logger.info("anthropic_block_completed", block_id=block["id"])
        return {"success": True, **result}

    except Exception as e:
        logger.error("anthropic_block_failed", block_id=block["id"], error=str(e))
        raise


async def _execute_message_completion(client: AsyncAnthropic, input_data: dict[str, Any]) -> dict[str, Any]:
    """Execute Anthropic message completion"""

    model = input_data.get("model", "claude-3-5-sonnet-20241022")
    messages = input_data.get("messages", [])

    # If messages is a string, convert to chat format
    if isinstance(messages, str):
        messages = [{"role": "user", "content": messages}]
    elif not isinstance(messages, list):
        messages = [{"role": "user", "content": str(messages)}]

    # Ensure messages have proper role structure for Anthropic
    # Anthropic requires alternating user/assistant messages
    formatted_messages = []
    for msg in messages:
        if isinstance(msg, dict):
            formatted_messages.append(msg)
        elif isinstance(msg, str):
            formatted_messages.append({"role": "user", "content": msg})

    # Extract system message if present (Anthropic uses separate system parameter)
    system_message = None
    if formatted_messages and formatted_messages[0].get("role") == "system":
        system_message = formatted_messages[0]["content"]
        formatted_messages = formatted_messages[1:]

    # Or check for system in input_data
    if not system_message:
        system_message = input_data.get("system")

    # Optional parameters
    max_tokens = input_data.get("max_tokens", 4096)
    temperature = input_data.get("temperature", 0.7)
    top_p = input_data.get("top_p")
    top_k = input_data.get("top_k")
    tools = input_data.get("tools")
    stream = input_data.get("stream", False)

    # Build request kwargs
    kwargs = {
        "model": model,
        "messages": formatted_messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    if system_message:
        kwargs["system"] = system_message
    if top_p is not None:
        kwargs["top_p"] = top_p
    if top_k is not None:
        kwargs["top_k"] = top_k
    if tools:
        kwargs["tools"] = tools
    if stream:
        kwargs["stream"] = stream

    # Make API call
    response = await client.messages.create(**kwargs)

    # Extract response content
    content = ""
    tool_uses = []

    for content_block in response.content:
        if hasattr(content_block, "text"):
            content += content_block.text
        elif hasattr(content_block, "tool_use"):
            tool_uses.append({
                "id": content_block.id,
                "name": content_block.name,
                "input": content_block.input,
            })

    result = {
        "content": content,
        "role": response.role,
        "model": response.model,
        "stop_reason": response.stop_reason,
        "usage": {
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
        },
    }

    # Include tool uses if present
    if tool_uses:
        result["tool_uses"] = tool_uses

    return result
