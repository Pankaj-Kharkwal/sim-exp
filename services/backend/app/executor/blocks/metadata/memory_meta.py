"""
Memory Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "memory",
    "name": "Memory",
    "description": "Add memory store",
    "long_description": """Integrate Memory into the workflow. Can add, get a memory, get all memories, and delete memories.""",
    "category": "blocks",
    "tools": [
        "memory_add",
        "memory_get",
        "memory_get_all",
        "memory_delete"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
