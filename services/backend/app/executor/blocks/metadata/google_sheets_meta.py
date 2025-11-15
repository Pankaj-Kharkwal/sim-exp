"""
Google Sheets Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "google_sheets",
    "name": "Google Sheets",
    "description": "Read, write, and update data",
    "long_description": """Integrate Google Sheets into the workflow. Can read, write, append, and update data.""",
    "category": "tools",
    "tools": [
        "google_sheets_read",
        "google_sheets_write",
        "google_sheets_update",
        "google_sheets_append"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
