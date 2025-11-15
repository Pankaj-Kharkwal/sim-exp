"""Gmail block executor - Email management and automation"""

from typing import Any, Optional
import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import httpx

from app.core.logging import get_logger
from app.executor.state import WorkflowState

logger = get_logger(__name__)


async def execute_gmail_block(
    block: dict[str, Any], input_data: dict[str, Any], state: WorkflowState
) -> dict[str, Any]:
    """
    Execute a Gmail block for email operations

    Supports:
    - Send emails (with attachments)
    - Read emails
    - Search emails
    - Mark as read/unread
    - Add/remove labels
    - Delete emails
    - Get email details
    """

    logger.info("gmail_block_executing", block_id=block["id"], action=input_data.get("action", "send_email"))

    # Get Gmail credentials (OAuth2 access token)
    access_token = input_data.get("access_token") or input_data.get("gmail_token") or os.getenv("GMAIL_ACCESS_TOKEN")
    if not access_token:
        raise ValueError("Gmail access token is required. Set GMAIL_ACCESS_TOKEN environment variable or provide in block config.")

    # Determine action
    action = input_data.get("action", "send_email").lower()

    try:
        if action == "send_email" or action == "send":
            result = await _send_email(access_token, input_data)
        elif action == "read_email" or action == "get_email":
            result = await _read_email(access_token, input_data)
        elif action == "search_emails" or action == "search":
            result = await _search_emails(access_token, input_data)
        elif action == "list_emails" or action == "list":
            result = await _list_emails(access_token, input_data)
        elif action == "mark_read":
            result = await _mark_as_read(access_token, input_data)
        elif action == "mark_unread":
            result = await _mark_as_unread(access_token, input_data)
        elif action == "add_label":
            result = await _add_label(access_token, input_data)
        elif action == "remove_label":
            result = await _remove_label(access_token, input_data)
        elif action == "delete_email" or action == "delete":
            result = await _delete_email(access_token, input_data)
        elif action == "get_labels":
            result = await _get_labels(access_token, input_data)
        else:
            raise ValueError(f"Unknown Gmail action: {action}")

        logger.info("gmail_block_completed", block_id=block["id"], action=action)
        return {"success": True, **result}

    except Exception as e:
        logger.error("gmail_block_failed", block_id=block["id"], error=str(e))
        raise


async def _send_email(access_token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Send an email via Gmail API"""

    to = input_data.get("to")
    subject = input_data.get("subject", "")
    body = input_data.get("body") or input_data.get("message", "")
    cc = input_data.get("cc")
    bcc = input_data.get("bcc")
    attachments = input_data.get("attachments", [])
    is_html = input_data.get("is_html", False)

    if not to:
        raise ValueError("Recipient email address (to) is required")

    # Create message
    if attachments:
        message = MIMEMultipart()
    else:
        message = MIMEText(body, "html" if is_html else "plain")
        message = MIMEMultipart()
        message.attach(MIMEText(body, "html" if is_html else "plain"))

    message["To"] = to if isinstance(to, str) else ", ".join(to)
    message["Subject"] = subject

    if cc:
        message["Cc"] = cc if isinstance(cc, str) else ", ".join(cc)
    if bcc:
        message["Bcc"] = bcc if isinstance(bcc, str) else ", ".join(bcc)

    # Add attachments if any
    for attachment in attachments:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.get("content", b""))
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {attachment.get('filename', 'file')}",
        )
        message.attach(part)

    # Encode message
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    # Send via Gmail API
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://gmail.googleapis.com/gmail/v1/users/me/messages/send",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
            json={"raw": raw_message},
            timeout=30.0,
        )

    if response.status_code != 200:
        raise Exception(f"Gmail API error: {response.text}")

    result = response.json()
    return {
        "message_id": result.get("id"),
        "thread_id": result.get("threadId"),
        "label_ids": result.get("labelIds", []),
    }


async def _read_email(access_token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Read a specific email by ID"""

    message_id = input_data.get("message_id") or input_data.get("id")
    if not message_id:
        raise ValueError("Message ID is required to read an email")

    format_type = input_data.get("format", "full")  # full, metadata, minimal, raw

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{message_id}",
            headers={"Authorization": f"Bearer {access_token}"},
            params={"format": format_type},
            timeout=30.0,
        )

    if response.status_code != 200:
        raise Exception(f"Gmail API error: {response.text}")

    message = response.json()

    # Parse headers
    headers = {}
    if "payload" in message and "headers" in message["payload"]:
        for header in message["payload"]["headers"]:
            headers[header["name"].lower()] = header["value"]

    # Extract body
    body = ""
    if "payload" in message:
        if "body" in message["payload"] and "data" in message["payload"]["body"]:
            body = base64.urlsafe_b64decode(message["payload"]["body"]["data"]).decode("utf-8")
        elif "parts" in message["payload"]:
            for part in message["payload"]["parts"]:
                if part.get("mimeType") == "text/plain" and "data" in part.get("body", {}):
                    body = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
                    break

    return {
        "message_id": message.get("id"),
        "thread_id": message.get("threadId"),
        "subject": headers.get("subject", ""),
        "from": headers.get("from", ""),
        "to": headers.get("to", ""),
        "date": headers.get("date", ""),
        "body": body,
        "snippet": message.get("snippet", ""),
        "label_ids": message.get("labelIds", []),
    }


async def _search_emails(access_token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Search emails using Gmail query syntax"""

    query = input_data.get("query") or input_data.get("q", "")
    max_results = input_data.get("max_results", 10)
    label_ids = input_data.get("label_ids")

    if not query and not label_ids:
        raise ValueError("Either query or label_ids is required to search emails")

    params = {
        "maxResults": max_results,
    }

    if query:
        params["q"] = query
    if label_ids:
        params["labelIds"] = label_ids if isinstance(label_ids, list) else [label_ids]

    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://gmail.googleapis.com/gmail/v1/users/me/messages",
            headers={"Authorization": f"Bearer {access_token}"},
            params=params,
            timeout=30.0,
        )

    if response.status_code != 200:
        raise Exception(f"Gmail API error: {response.text}")

    result = response.json()
    messages = result.get("messages", [])

    return {
        "messages": [{"id": msg["id"], "thread_id": msg["threadId"]} for msg in messages],
        "count": len(messages),
        "result_size_estimate": result.get("resultSizeEstimate", 0),
    }


async def _list_emails(access_token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """List emails with optional filters"""

    max_results = input_data.get("max_results", 100)
    label_ids = input_data.get("label_ids", ["INBOX"])
    include_spam_trash = input_data.get("include_spam_trash", False)

    params = {
        "maxResults": max_results,
        "labelIds": label_ids if isinstance(label_ids, list) else [label_ids],
        "includeSpamTrash": include_spam_trash,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://gmail.googleapis.com/gmail/v1/users/me/messages",
            headers={"Authorization": f"Bearer {access_token}"},
            params=params,
            timeout=30.0,
        )

    if response.status_code != 200:
        raise Exception(f"Gmail API error: {response.text}")

    result = response.json()
    messages = result.get("messages", [])

    return {
        "messages": [{"id": msg["id"], "thread_id": msg["threadId"]} for msg in messages],
        "count": len(messages),
    }


async def _mark_as_read(access_token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Mark email as read"""

    message_id = input_data.get("message_id") or input_data.get("id")
    if not message_id:
        raise ValueError("Message ID is required")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{message_id}/modify",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
            json={"removeLabelIds": ["UNREAD"]},
            timeout=30.0,
        )

    if response.status_code != 200:
        raise Exception(f"Gmail API error: {response.text}")

    return {"marked_as_read": True, "message_id": message_id}


async def _mark_as_unread(access_token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Mark email as unread"""

    message_id = input_data.get("message_id") or input_data.get("id")
    if not message_id:
        raise ValueError("Message ID is required")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{message_id}/modify",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
            json={"addLabelIds": ["UNREAD"]},
            timeout=30.0,
        )

    if response.status_code != 200:
        raise Exception(f"Gmail API error: {response.text}")

    return {"marked_as_unread": True, "message_id": message_id}


async def _add_label(access_token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Add label to email"""

    message_id = input_data.get("message_id") or input_data.get("id")
    label_ids = input_data.get("label_ids") or input_data.get("labels")

    if not message_id or not label_ids:
        raise ValueError("Message ID and label_ids are required")

    if isinstance(label_ids, str):
        label_ids = [label_ids]

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{message_id}/modify",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
            json={"addLabelIds": label_ids},
            timeout=30.0,
        )

    if response.status_code != 200:
        raise Exception(f"Gmail API error: {response.text}")

    return {"labels_added": True, "message_id": message_id, "label_ids": label_ids}


async def _remove_label(access_token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Remove label from email"""

    message_id = input_data.get("message_id") or input_data.get("id")
    label_ids = input_data.get("label_ids") or input_data.get("labels")

    if not message_id or not label_ids:
        raise ValueError("Message ID and label_ids are required")

    if isinstance(label_ids, str):
        label_ids = [label_ids]

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{message_id}/modify",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
            json={"removeLabelIds": label_ids},
            timeout=30.0,
        )

    if response.status_code != 200:
        raise Exception(f"Gmail API error: {response.text}")

    return {"labels_removed": True, "message_id": message_id, "label_ids": label_ids}


async def _delete_email(access_token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Delete an email permanently"""

    message_id = input_data.get("message_id") or input_data.get("id")
    if not message_id:
        raise ValueError("Message ID is required")

    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{message_id}",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=30.0,
        )

    if response.status_code != 204:
        raise Exception(f"Gmail API error: {response.text}")

    return {"deleted": True, "message_id": message_id}


async def _get_labels(access_token: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Get all Gmail labels"""

    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://gmail.googleapis.com/gmail/v1/users/me/labels",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=30.0,
        )

    if response.status_code != 200:
        raise Exception(f"Gmail API error: {response.text}")

    result = response.json()
    labels = result.get("labels", [])

    return {
        "labels": [
            {
                "id": label.get("id"),
                "name": label.get("name"),
                "type": label.get("type"),
                "message_list_visibility": label.get("messageListVisibility"),
                "label_list_visibility": label.get("labelListVisibility"),
            }
            for label in labels
        ],
        "count": len(labels),
    }
