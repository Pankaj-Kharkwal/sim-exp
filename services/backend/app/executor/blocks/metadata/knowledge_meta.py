"""
Knowledge Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "knowledge",
    "name": "Knowledge",
    "description": "Use vector search",
    "long_description": """Integrate Knowledge into the workflow. Can search, upload chunks, and create documents.""",
    "category": "blocks",
    "tools": [
        "knowledge_search",
        "knowledge_upload_chunk",
        "knowledge_create_document"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
