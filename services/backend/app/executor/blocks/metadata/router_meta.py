"""
Router Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "router",
    "name": "Router",
    "description": "Route workflow",
    "long_description": """This is a core workflow block. Intelligently direct workflow execution to different paths based on input analysis. Use natural language to instruct the router to route to certain blocks based on the input.""",
    "category": "blocks",
    "tools": [
        "openai_chat",
        "anthropic_chat",
        "google_chat",
        "xai_chat",
        "deepseek_chat",
        "deepseek_reasoner"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
