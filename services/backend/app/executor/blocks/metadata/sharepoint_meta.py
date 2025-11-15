"""
Sharepoint Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "sharepoint",
    "name": "Sharepoint",
    "description": "Work with pages and lists",
    "long_description": """Integrate SharePoint into the workflow. Read/create pages, list sites, and work with lists (read, create, update items). Requires OAuth.""",
    "category": "tools",
    "tools": [
        "sharepoint_create_page",
        "sharepoint_read_page",
        "sharepoint_list_sites",
        "sharepoint_create_list",
        "sharepoint_get_list",
        "sharepoint_update_list",
        "sharepoint_add_list_items",
        "sharepoint_upload_file"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
