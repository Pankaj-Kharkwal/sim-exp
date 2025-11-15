"""
Thinking Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "thinking",
    "name": "Thinking",
    "description": "Forces model to outline its thought process.",
    "long_description": """Adds a step where the model explicitly outlines its thought process before proceeding. This can improve reasoning quality by encouraging step-by-step analysis.""",
    "category": "tools",
    "tools": [
        "thinking_tool"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
