"""
Mem0 Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "mem0",
    "name": "Mem0",
    "description": "Agent memory management",
    "long_description": """Integrate Mem0 into the workflow. Can add, search, and retrieve memories.""",
    "category": "tools",
    "tools": [
        "mem0_add_memories",
        "mem0_search_memories",
        "mem0_get_memories"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
