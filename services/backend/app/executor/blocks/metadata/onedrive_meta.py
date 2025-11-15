"""
OneDrive Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "onedrive",
    "name": "OneDrive",
    "description": "Create, upload, and list files",
    "long_description": """Integrate OneDrive into the workflow. Can create text and Excel files, upload files, and list files.""",
    "category": "tools",
    "tools": [
        "onedrive_upload",
        "onedrive_create_folder",
        "onedrive_list"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
