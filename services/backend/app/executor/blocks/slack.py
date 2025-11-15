"""Slack block executor - Team communication and messaging"""

from typing import Any, Optional
import os
import httpx

from app.core.logging import get_logger
from app.executor.state import WorkflowState

logger = get_logger(__name__)


async def execute_slack_block(
    block: dict[str, Any], input_data: dict[str, Any], state: WorkflowState
) -> dict[str, Any]:
    """
    Execute a Slack block for messaging and communication

    Supports:
    - Send messages to channels
    - Send direct messages to users
    - Post file uploads
    - Update messages
    - Add reactions
    - Get channel info
    - List channels
    """

    logger.info("slack_block_executing", block_id=block["id"], action=input_data.get("action", "send_message"))

    # Get Slack token
    token = input_data.get("token") or input_data.get("slack_token") or os.getenv("SLACK_BOT_TOKEN")
    if not token:
        raise ValueError("Slack token is required. Set SLACK_BOT_TOKEN environment variable or provide in block config.")

    # Determine action
    action = input_data.get("action", "send_message").lower()

    try:
        if action == "send_message" or action == "post_message":
            result = await _send_message(token, input_data)
        elif action == "update_message":
            result = await _update_message(token, input_data)
        elif action == "upload_file":
            result = await _upload_file(token, input_data)
        elif action == "add_reaction":
            result = await _add_reaction(token, input_data)
        elif action == "list_channels":
            result = await _list_channels(token, input_data)
        elif action == "get_channel_info":
            result = await _get_channel_info(token, input_data)
        else:
            raise ValueError(f"Unknown Slack action: {action}")

        logger.info("slack_block_completed", block_id=block["id"], action=action)
        return {"success": True, **result}

    except Exception as e:
        logger.error("slack_block_failed", block_id=block["id"], error=str(e))
        raise


async def _send_message(token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Send a message to a Slack channel or user"""

    channel = input_data.get("channel")
    text = input_data.get("text") or input_data.get("message")
    blocks = input_data.get("blocks")
    thread_ts = input_data.get("thread_ts")
    username = input_data.get("username")
    icon_emoji = input_data.get("icon_emoji")

    if not channel:
        raise ValueError("Channel is required to send a message")
    if not text and not blocks:
        raise ValueError("Either text or blocks are required to send a message")

    # Build request payload
    payload = {
        "channel": channel,
    }

    if text:
        payload["text"] = text
    if blocks:
        payload["blocks"] = blocks
    if thread_ts:
        payload["thread_ts"] = thread_ts
    if username:
        payload["username"] = username
    if icon_emoji:
        payload["icon_emoji"] = icon_emoji

    # Make API call
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://slack.com/api/chat.postMessage",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30.0,
        )

    result = response.json()

    if not result.get("ok"):
        error = result.get("error", "Unknown error")
        raise Exception(f"Slack API error: {error}")

    return {
        "message_ts": result.get("ts"),
        "channel": result.get("channel"),
        "message": result.get("message"),
    }


async def _update_message(token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Update an existing Slack message"""

    channel = input_data.get("channel")
    ts = input_data.get("ts") or input_data.get("message_ts")
    text = input_data.get("text")
    blocks = input_data.get("blocks")

    if not channel or not ts:
        raise ValueError("Channel and message timestamp (ts) are required to update a message")
    if not text and not blocks:
        raise ValueError("Either text or blocks are required to update a message")

    payload = {
        "channel": channel,
        "ts": ts,
    }

    if text:
        payload["text"] = text
    if blocks:
        payload["blocks"] = blocks

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://slack.com/api/chat.update",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30.0,
        )

    result = response.json()

    if not result.get("ok"):
        error = result.get("error", "Unknown error")
        raise Exception(f"Slack API error: {error}")

    return {
        "message_ts": result.get("ts"),
        "channel": result.get("channel"),
    }


async def _upload_file(token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Upload a file to Slack"""

    channels = input_data.get("channels")
    file_content = input_data.get("file") or input_data.get("content")
    filename = input_data.get("filename", "file.txt")
    title = input_data.get("title")
    initial_comment = input_data.get("initial_comment")

    if not file_content:
        raise ValueError("File content is required to upload a file")

    # Prepare multipart form data
    files = {"file": (filename, file_content)}

    data = {}
    if channels:
        data["channels"] = channels if isinstance(channels, str) else ",".join(channels)
    if title:
        data["title"] = title
    if initial_comment:
        data["initial_comment"] = initial_comment

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://slack.com/api/files.upload",
            headers={"Authorization": f"Bearer {token}"},
            files=files,
            data=data,
            timeout=60.0,
        )

    result = response.json()

    if not result.get("ok"):
        error = result.get("error", "Unknown error")
        raise Exception(f"Slack API error: {error}")

    return {
        "file_id": result.get("file", {}).get("id"),
        "url": result.get("file", {}).get("url_private"),
    }


async def _add_reaction(token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Add a reaction emoji to a message"""

    channel = input_data.get("channel")
    timestamp = input_data.get("timestamp") or input_data.get("ts")
    reaction = input_data.get("reaction") or input_data.get("emoji")

    if not channel or not timestamp or not reaction:
        raise ValueError("Channel, timestamp, and reaction are required")

    # Remove colons if present
    reaction = reaction.strip(":")

    payload = {
        "channel": channel,
        "timestamp": timestamp,
        "name": reaction,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://slack.com/api/reactions.add",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30.0,
        )

    result = response.json()

    if not result.get("ok"):
        error = result.get("error", "Unknown error")
        raise Exception(f"Slack API error: {error}")

    return {"added": True, "reaction": reaction}


async def _list_channels(token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """List Slack channels"""

    exclude_archived = input_data.get("exclude_archived", True)
    limit = input_data.get("limit", 100)

    payload = {
        "exclude_archived": exclude_archived,
        "limit": limit,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://slack.com/api/conversations.list",
            headers={"Authorization": f"Bearer {token}"},
            params=payload,
            timeout=30.0,
        )

    result = response.json()

    if not result.get("ok"):
        error = result.get("error", "Unknown error")
        raise Exception(f"Slack API error: {error}")

    channels = result.get("channels", [])
    return {
        "channels": [
            {
                "id": ch.get("id"),
                "name": ch.get("name"),
                "is_private": ch.get("is_private", False),
                "is_archived": ch.get("is_archived", False),
            }
            for ch in channels
        ],
        "count": len(channels),
    }


async def _get_channel_info(token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Get information about a Slack channel"""

    channel = input_data.get("channel")
    if not channel:
        raise ValueError("Channel is required to get channel info")

    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://slack.com/api/conversations.info",
            headers={"Authorization": f"Bearer {token}"},
            params={"channel": channel},
            timeout=30.0,
        )

    result = response.json()

    if not result.get("ok"):
        error = result.get("error", "Unknown error")
        raise Exception(f"Slack API error: {error}")

    channel_info = result.get("channel", {})
    return {
        "id": channel_info.get("id"),
        "name": channel_info.get("name"),
        "topic": channel_info.get("topic", {}).get("value"),
        "purpose": channel_info.get("purpose", {}).get("value"),
        "is_private": channel_info.get("is_private", False),
        "is_archived": channel_info.get("is_archived", False),
        "num_members": channel_info.get("num_members"),
    }
