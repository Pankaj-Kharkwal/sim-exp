"""
Outlook Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "outlook",
    "name": "Outlook",
    "description": "Access Outlook",
    "long_description": """Integrate Outlook into the workflow. Can read, draft, and send email messages. Can be used in trigger mode to trigger a workflow when a new email is received.""",
    "category": "tools",
    "tools": [
        "outlook_send",
        "outlook_draft",
        "outlook_read",
        "outlook_forward"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
