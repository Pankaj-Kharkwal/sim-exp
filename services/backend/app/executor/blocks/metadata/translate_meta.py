"""
Translate Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "translate",
    "name": "Translate",
    "description": "Translate text to any language",
    "long_description": """Integrate Translate into the workflow. Can translate text to any language.""",
    "category": "tools",
    "tools": [
        "openai_chat",
        "anthropic_chat",
        "google_chat"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
