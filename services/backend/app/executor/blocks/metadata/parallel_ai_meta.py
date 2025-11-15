"""
Parallel AI Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "parallel_ai",
    "name": "Parallel AI",
    "description": "Search with Parallel AI",
    "long_description": """Integrate Parallel AI into the workflow. Can search the web.""",
    "category": "tools",
    "tools": [
        "parallel_search"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
