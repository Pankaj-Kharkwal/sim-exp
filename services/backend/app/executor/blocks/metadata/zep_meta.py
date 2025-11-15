"""
Zep Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "zep",
    "name": "Zep",
    "description": "Long-term memory for AI agents",
    "long_description": """Integrate Zep for long-term memory management. Create threads, add messages, retrieve context with AI-powered summaries and facts extraction.""",
    "category": "tools",
    "tools": [
        "zep_create_thread",
        "zep_get_threads",
        "zep_delete_thread",
        "zep_get_context",
        "zep_get_messages",
        "zep_add_messages",
        "zep_add_user",
        "zep_get_user",
        "zep_get_user_threads"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
