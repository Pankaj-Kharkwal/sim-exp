"""
Jina Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "jina",
    "name": "Jina",
    "description": "Convert website content into text",
    "long_description": """Integrate Jina into the workflow. Extracts content from websites.""",
    "category": "tools",
    "tools": [
        "jina_read_url"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
