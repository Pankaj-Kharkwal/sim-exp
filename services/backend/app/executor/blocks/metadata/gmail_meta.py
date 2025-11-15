"""
Gmail Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "gmail",
    "name": "Gmail",
    "description": "Send Gmail or trigger workflows from Gmail events",
    "long_description": """Integrate Gmail into the workflow. Can send, read, and search emails. Can be used in trigger mode to trigger a workflow when a new email is received.""",
    "category": "tools",
    "tools": [
        "gmail_send",
        "gmail_draft",
        "gmail_read",
        "gmail_search"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
