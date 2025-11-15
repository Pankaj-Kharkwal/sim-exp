"""
Webflow Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "webflow",
    "name": "Webflow",
    "description": "Manage Webflow CMS collections",
    "long_description": """Integrates Webflow CMS into the workflow. Can create, get, list, update, or delete items in Webflow CMS collections. Manage your Webflow content programmatically. Can be used in trigger mode to trigger workflows when collection items change or forms are submitted.""",
    "category": "tools",
    "tools": [
        "webflow_list_items",
        "webflow_get_item",
        "webflow_create_item",
        "webflow_update_item",
        "webflow_delete_item"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
