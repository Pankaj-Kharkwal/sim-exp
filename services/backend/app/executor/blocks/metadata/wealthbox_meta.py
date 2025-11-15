"""
Wealthbox Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "wealthbox",
    "name": "Wealthbox",
    "description": "Interact with Wealthbox",
    "long_description": """Integrate Wealthbox into the workflow. Can read and write notes, read and write contacts, and read and write tasks.""",
    "category": "tools",
    "tools": [
        "wealthbox_read_note",
        "wealthbox_write_note",
        "wealthbox_read_contact",
        "wealthbox_write_contact",
        "wealthbox_read_task",
        "wealthbox_write_task"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
