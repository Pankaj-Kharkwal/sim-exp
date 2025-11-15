"""
Notion Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "notion",
    "name": "Notion",
    "description": "Manage Notion pages",
    "long_description": """Integrate with Notion into the workflow. Can read page, read database, create page, create database, append content, query database, and search workspace.""",
    "category": "tools",
    "tools": [
        "notion_read",
        "notion_read_database",
        "notion_write",
        "notion_create_page",
        "notion_query_database",
        "notion_search",
        "notion_create_database"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
