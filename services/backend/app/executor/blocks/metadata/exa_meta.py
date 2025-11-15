"""
Exa Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "exa",
    "name": "Exa",
    "description": "Search with Exa AI",
    "long_description": """Integrate Exa into the workflow. Can search, get contents, find similar links, answer a question, and perform research.""",
    "category": "tools",
    "tools": [
        "exa_search",
        "exa_get_contents",
        "exa_find_similar_links",
        "exa_answer",
        "exa_research"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
