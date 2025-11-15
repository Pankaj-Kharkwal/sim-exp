"""
X Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "x",
    "name": "X",
    "description": "Interact with X",
    "long_description": """Integrate X into the workflow. Can post a new tweet, get tweet details, search tweets, and get user profile.""",
    "category": "tools",
    "tools": [
        "x_write",
        "x_read",
        "x_search",
        "x_user"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
