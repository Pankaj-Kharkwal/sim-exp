"""
Google Drive Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "google_drive",
    "name": "Google Drive",
    "description": "Create, upload, and list files",
    "long_description": """Integrate Google Drive into the workflow. Can create, upload, and list files.""",
    "category": "tools",
    "tools": [
        "google_drive_upload",
        "google_drive_create_folder",
        "google_drive_list"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
