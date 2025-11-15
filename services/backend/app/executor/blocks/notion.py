"""Notion block executor - Knowledge base and database management"""

from typing import Any, Optional
import os
import httpx

from app.core.logging import get_logger
from app.executor.state import WorkflowState

logger = get_logger(__name__)


async def execute_notion_block(
    block: dict[str, Any], input_data: dict[str, Any], state: WorkflowState
) -> dict[str, Any]:
    """
    Execute a Notion block for database and page operations

    Supports:
    - Database operations (query, create items, update items)
    - Page operations (create, update, get)
    - Block operations (get children, append)
    - Search across workspace
    - User management
    """

    logger.info("notion_block_executing", block_id=block["id"], action=input_data.get("action", "query_database"))

    # Get Notion API key
    api_key = input_data.get("api_key") or input_data.get("notion_key") or os.getenv("NOTION_API_KEY")
    if not api_key:
        raise ValueError("Notion API key is required. Set NOTION_API_KEY environment variable or provide in block config.")

    # Determine action
    action = input_data.get("action", "query_database").lower()

    try:
        if action == "query_database" or action == "query":
            result = await _query_database(api_key, input_data)
        elif action == "create_page" or action == "create":
            result = await _create_page(api_key, input_data)
        elif action == "update_page" or action == "update":
            result = await _update_page(api_key, input_data)
        elif action == "get_page":
            result = await _get_page(api_key, input_data)
        elif action == "get_database":
            result = await _get_database(api_key, input_data)
        elif action == "get_block_children" or action == "get_blocks":
            result = await _get_block_children(api_key, input_data)
        elif action == "append_blocks" or action == "append":
            result = await _append_blocks(api_key, input_data)
        elif action == "search":
            result = await _search(api_key, input_data)
        else:
            raise ValueError(f"Unknown Notion action: {action}")

        logger.info("notion_block_completed", block_id=block["id"], action=action)
        return {"success": True, **result}

    except Exception as e:
        logger.error("notion_block_failed", block_id=block["id"], error=str(e))
        raise


async def _query_database(api_key: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Query a Notion database"""

    database_id = input_data.get("database_id")
    filter_obj = input_data.get("filter")
    sorts = input_data.get("sorts")
    page_size = input_data.get("page_size", 100)

    if not database_id:
        raise ValueError("Database ID is required")

    payload = {
        "page_size": page_size,
    }

    if filter_obj:
        payload["filter"] = filter_obj
    if sorts:
        payload["sorts"] = sorts

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.notion.com/v1/databases/{database_id}/query",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Notion-Version": "2022-06-28",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30.0,
        )

    if response.status_code != 200:
        raise Exception(f"Notion API error: {response.text}")

    result = response.json()
    results = result.get("results", [])

    return {
        "pages": [
            {
                "id": page.get("id"),
                "properties": page.get("properties", {}),
                "created_time": page.get("created_time"),
                "last_edited_time": page.get("last_edited_time"),
                "url": page.get("url"),
            }
            for page in results
        ],
        "count": len(results),
        "has_more": result.get("has_more", False),
        "next_cursor": result.get("next_cursor"),
    }


async def _create_page(api_key: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Create a new Notion page"""

    parent = input_data.get("parent")
    properties = input_data.get("properties", {})
    children = input_data.get("children")  # Block content
    icon = input_data.get("icon")
    cover = input_data.get("cover")

    if not parent:
        raise ValueError("Parent (database_id or page_id) is required")

    # Build parent object
    if isinstance(parent, str):
        # Assume it's a database ID
        parent_obj = {"database_id": parent}
    else:
        parent_obj = parent

    payload = {
        "parent": parent_obj,
        "properties": properties,
    }

    if children:
        payload["children"] = children
    if icon:
        payload["icon"] = icon
    if cover:
        payload["cover"] = cover

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.notion.com/v1/pages",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Notion-Version": "2022-06-28",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30.0,
        )

    if response.status_code not in [200, 201]:
        raise Exception(f"Notion API error: {response.text}")

    page = response.json()
    return {
        "page_id": page.get("id"),
        "url": page.get("url"),
        "created_time": page.get("created_time"),
        "properties": page.get("properties", {}),
    }


async def _update_page(api_key: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Update an existing Notion page"""

    page_id = input_data.get("page_id") or input_data.get("id")
    properties = input_data.get("properties")
    icon = input_data.get("icon")
    cover = input_data.get("cover")
    archived = input_data.get("archived")

    if not page_id:
        raise ValueError("Page ID is required")

    payload = {}

    if properties:
        payload["properties"] = properties
    if icon:
        payload["icon"] = icon
    if cover:
        payload["cover"] = cover
    if archived is not None:
        payload["archived"] = archived

    async with httpx.AsyncClient() as client:
        response = await client.patch(
            f"https://api.notion.com/v1/pages/{page_id}",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Notion-Version": "2022-06-28",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30.0,
        )

    if response.status_code != 200:
        raise Exception(f"Notion API error: {response.text}")

    page = response.json()
    return {
        "page_id": page.get("id"),
        "url": page.get("url"),
        "last_edited_time": page.get("last_edited_time"),
        "properties": page.get("properties", {}),
        "archived": page.get("archived", False),
    }


async def _get_page(api_key: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Get a Notion page by ID"""

    page_id = input_data.get("page_id") or input_data.get("id")

    if not page_id:
        raise ValueError("Page ID is required")

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.notion.com/v1/pages/{page_id}",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Notion-Version": "2022-06-28",
            },
            timeout=30.0,
        )

    if response.status_code != 200:
        raise Exception(f"Notion API error: {response.text}")

    page = response.json()
    return {
        "page_id": page.get("id"),
        "created_time": page.get("created_time"),
        "last_edited_time": page.get("last_edited_time"),
        "url": page.get("url"),
        "properties": page.get("properties", {}),
        "parent": page.get("parent", {}),
        "archived": page.get("archived", False),
    }


async def _get_database(api_key: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Get a Notion database by ID"""

    database_id = input_data.get("database_id") or input_data.get("id")

    if not database_id:
        raise ValueError("Database ID is required")

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.notion.com/v1/databases/{database_id}",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Notion-Version": "2022-06-28",
            },
            timeout=30.0,
        )

    if response.status_code != 200:
        raise Exception(f"Notion API error: {response.text}")

    database = response.json()
    return {
        "database_id": database.get("id"),
        "title": database.get("title", []),
        "description": database.get("description", []),
        "created_time": database.get("created_time"),
        "last_edited_time": database.get("last_edited_time"),
        "url": database.get("url"),
        "properties": database.get("properties", {}),
    }


async def _get_block_children(api_key: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Get children blocks of a page or block"""

    block_id = input_data.get("block_id") or input_data.get("page_id") or input_data.get("id")
    page_size = input_data.get("page_size", 100)

    if not block_id:
        raise ValueError("Block ID or Page ID is required")

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.notion.com/v1/blocks/{block_id}/children",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Notion-Version": "2022-06-28",
            },
            params={"page_size": page_size},
            timeout=30.0,
        )

    if response.status_code != 200:
        raise Exception(f"Notion API error: {response.text}")

    result = response.json()
    blocks = result.get("results", [])

    return {
        "blocks": [
            {
                "id": block.get("id"),
                "type": block.get("type"),
                "created_time": block.get("created_time"),
                "last_edited_time": block.get("last_edited_time"),
                "has_children": block.get("has_children", False),
                "content": block.get(block.get("type", ""), {}),
            }
            for block in blocks
        ],
        "count": len(blocks),
        "has_more": result.get("has_more", False),
        "next_cursor": result.get("next_cursor"),
    }


async def _append_blocks(api_key: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Append block children to a page or block"""

    block_id = input_data.get("block_id") or input_data.get("page_id") or input_data.get("id")
    children = input_data.get("children") or input_data.get("blocks")

    if not block_id:
        raise ValueError("Block ID or Page ID is required")
    if not children:
        raise ValueError("Children blocks are required")

    payload = {
        "children": children,
    }

    async with httpx.AsyncClient() as client:
        response = await client.patch(
            f"https://api.notion.com/v1/blocks/{block_id}/children",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Notion-Version": "2022-06-28",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30.0,
        )

    if response.status_code != 200:
        raise Exception(f"Notion API error: {response.text}")

    result = response.json()
    blocks = result.get("results", [])

    return {
        "blocks_added": len(blocks),
        "blocks": [
            {
                "id": block.get("id"),
                "type": block.get("type"),
            }
            for block in blocks
        ],
    }


async def _search(api_key: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Search across Notion workspace"""

    query = input_data.get("query", "")
    filter_obj = input_data.get("filter")  # {"value": "page"} or {"value": "database"}
    sort = input_data.get("sort")
    page_size = input_data.get("page_size", 100)

    payload = {
        "page_size": page_size,
    }

    if query:
        payload["query"] = query
    if filter_obj:
        payload["filter"] = filter_obj
    if sort:
        payload["sort"] = sort

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.notion.com/v1/search",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Notion-Version": "2022-06-28",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30.0,
        )

    if response.status_code != 200:
        raise Exception(f"Notion API error: {response.text}")

    result = response.json()
    results = result.get("results", [])

    return {
        "results": [
            {
                "id": item.get("id"),
                "object": item.get("object"),  # page or database
                "url": item.get("url"),
                "created_time": item.get("created_time"),
                "last_edited_time": item.get("last_edited_time"),
            }
            for item in results
        ],
        "count": len(results),
        "has_more": result.get("has_more", False),
        "next_cursor": result.get("next_cursor"),
    }
