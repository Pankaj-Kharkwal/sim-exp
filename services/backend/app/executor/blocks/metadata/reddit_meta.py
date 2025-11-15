"""
Reddit Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "reddit",
    "name": "Reddit",
    "description": "Access Reddit data and content",
    "long_description": """Integrate Reddit into the workflow. Can get posts and comments from a subreddit.""",
    "category": "tools",
    "tools": [
        "reddit_get_posts",
        "reddit_get_comments"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
