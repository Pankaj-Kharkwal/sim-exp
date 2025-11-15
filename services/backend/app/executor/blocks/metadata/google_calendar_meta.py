"""
Google Calendar Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "google_calendar",
    "name": "Google Calendar",
    "description": "Manage Google Calendar events",
    "long_description": """Integrate Google Calendar into the workflow. Can create, read, update, and list calendar events.""",
    "category": "tools",
    "tools": [
        "google_calendar_create",
        "google_calendar_list",
        "google_calendar_get",
        "google_calendar_quick_add",
        "google_calendar_invite"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
