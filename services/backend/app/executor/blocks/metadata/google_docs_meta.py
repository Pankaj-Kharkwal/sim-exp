"""
Google Docs Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "google_docs",
    "name": "Google Docs",
    "description": "Read, write, and create documents",
    "long_description": """Integrate Google Docs into the workflow. Can read, write, and create documents.""",
    "category": "tools",
    "tools": [
        "google_docs_read",
        "google_docs_write",
        "google_docs_create"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
