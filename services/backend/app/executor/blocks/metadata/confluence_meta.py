"""
Confluence Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "confluence",
    "name": "Confluence",
    "description": "Interact with Confluence",
    "long_description": """Integrate Confluence into the workflow. Can read and update a page.""",
    "category": "tools",
    "tools": [
        "confluence_retrieve",
        "confluence_update"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
