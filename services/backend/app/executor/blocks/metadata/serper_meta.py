"""
Serper Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "serper",
    "name": "Serper",
    "description": "Search the web using Serper",
    "long_description": """Integrate Serper into the workflow. Can search the web.""",
    "category": "tools",
    "tools": [
        "serper_search"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
