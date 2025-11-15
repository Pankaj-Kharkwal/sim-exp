"""
Chat Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "chat_trigger",
    "name": "Chat",
    "description": "Start workflow from a chat deployment",
    "long_description": """Chat trigger to run the workflow via deployed chat interfaces.""",
    "category": "triggers",
    "tools": [],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
