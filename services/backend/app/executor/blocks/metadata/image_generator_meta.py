"""
Image Generator Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "image_generator",
    "name": "Image Generator",
    "description": "Generate images",
    "long_description": """Integrate Image Generator into the workflow. Can generate images using DALL-E 3 or GPT Image.""",
    "category": "tools",
    "tools": [
        "openai_image"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
