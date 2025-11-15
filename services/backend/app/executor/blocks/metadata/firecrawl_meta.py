"""
Firecrawl Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "firecrawl",
    "name": "Firecrawl",
    "description": "Scrape or search the web",
    "long_description": """Integrate Firecrawl into the workflow. Can search, scrape, or crawl websites.""",
    "category": "tools",
    "tools": [
        "firecrawl_scrape",
        "firecrawl_search",
        "firecrawl_crawl"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
