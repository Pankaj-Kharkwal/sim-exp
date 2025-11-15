"""
Tavily Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "tavily",
    "name": "Tavily",
    "description": "Search and extract information",
    "long_description": """Integrate Tavily into the workflow. Can search the web and extract content from specific URLs. Requires API Key.""",
    "category": "tools",
    "tools": [
        "tavily_search",
        "tavily_extract"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
