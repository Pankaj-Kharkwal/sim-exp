"""
MongoDB Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "mongodb",
    "name": "MongoDB",
    "description": "Connect to MongoDB database",
    "long_description": """Integrate MongoDB into the workflow. Can find, insert, update, delete, and aggregate data.""",
    "category": "tools",
    "tools": [
        "mongodb_query",
        "mongodb_insert",
        "mongodb_update",
        "mongodb_delete",
        "mongodb_execute"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
