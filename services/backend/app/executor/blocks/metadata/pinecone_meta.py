"""
Pinecone Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "pinecone",
    "name": "Pinecone",
    "description": "Use Pinecone vector database",
    "long_description": """Integrate Pinecone into the workflow. Can generate embeddings, upsert text, search with text, fetch vectors, and search with vectors.""",
    "category": "tools",
    "tools": [
        "pinecone_generate_embeddings",
        "pinecone_upsert_text",
        "pinecone_search_text",
        "pinecone_search_vector",
        "pinecone_fetch"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
