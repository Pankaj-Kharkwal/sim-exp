"""
Vision Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "vision",
    "name": "Vision",
    "description": "Analyze images with vision models",
    "long_description": """Integrate Vision into the workflow. Can analyze images with vision models.""",
    "category": "tools",
    "tools": [
        "vision_tool"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
