"""
evaluation_response Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "number",
    "name": "evaluation_response",
    "description": "Evaluate content",
    "long_description": """This is a core workflow block. Assess content quality using customizable evaluation metrics and scoring criteria. Create objective evaluation frameworks with numeric scoring to measure performance across multiple dimensions.""",
    "category": "tools",
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
