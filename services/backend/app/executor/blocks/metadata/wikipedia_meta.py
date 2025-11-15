"""
Wikipedia Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "wikipedia",
    "name": "Wikipedia",
    "description": "Search and retrieve content from Wikipedia",
    "long_description": """Integrate Wikipedia into the workflow. Can get page summary, search pages, get page content, and get random page.""",
    "category": "tools",
    "tools": [
        "wikipedia_summary",
        "wikipedia_search",
        "wikipedia_content",
        "wikipedia_random"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
