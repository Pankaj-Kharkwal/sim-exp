"""
Jira Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "jira",
    "name": "Jira",
    "description": "Interact with Jira",
    "long_description": """Integrate Jira into the workflow. Can read, write, and update issues.""",
    "category": "tools",
    "tools": [
        "jira_retrieve",
        "jira_update",
        "jira_write",
        "jira_bulk_read"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
