"""
ArXiv Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "arxiv",
    "name": "ArXiv",
    "description": "Search and retrieve academic papers from ArXiv",
    "long_description": """Integrates ArXiv into the workflow. Can search for papers, get paper details, and get author papers. Does not require OAuth or an API key.""",
    "category": "tools",
    "tools": [
        "arxiv_search",
        "arxiv_get_paper",
        "arxiv_get_author_papers"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
