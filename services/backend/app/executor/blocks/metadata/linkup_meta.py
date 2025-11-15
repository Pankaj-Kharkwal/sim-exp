"""
Linkup Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "linkup",
    "name": "Linkup",
    "description": "Search the web with Linkup",
    "long_description": """Integrate Linkup into the workflow. Can search the web.""",
    "category": "tools",
    "tools": [
        "linkup_search"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
