"""
Google Search Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "google_search",
    "name": "Google Search",
    "description": "Search the web",
    "long_description": """Integrate Google Search into the workflow. Can search the web.""",
    "category": "tools",
    "tools": [
        "google_search"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
