"""
Hugging Face Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "huggingface",
    "name": "Hugging Face",
    "description": "Use Hugging Face Inference API",
    "long_description": """Integrate Hugging Face into the workflow. Can generate completions using the Hugging Face Inference API.""",
    "category": "tools",
    "tools": [
        "huggingface_chat"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
