"""
Qdrant Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "qdrant",
    "name": "Qdrant",
    "description": "Use Qdrant vector database",
    "long_description": """Integrate Qdrant into the workflow. Can upsert, search, and fetch points.""",
    "category": "tools",
    "tools": [
        "qdrant_upsert_points",
        "qdrant_search_vector",
        "qdrant_fetch_points"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
