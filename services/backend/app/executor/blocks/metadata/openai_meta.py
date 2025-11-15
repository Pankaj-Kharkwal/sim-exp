"""
Embeddings Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "openai",
    "name": "Embeddings",
    "description": "Generate Open AI embeddings",
    "long_description": """Integrate Embeddings into the workflow. Can generate embeddings from text.""",
    "category": "tools",
    "tools": [
        "openai_embeddings"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
