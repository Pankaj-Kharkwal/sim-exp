"""
API Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "api",
    "name": "API",
    "description": "Use any API",
    "long_description": """This is a core workflow block. Connect to any external API with support for all standard HTTP methods and customizable request parameters. Configure headers, query parameters, and request bodies. Standard headers (User-Agent, Accept, Cache-Control, etc.) are automatically included.""",
    "category": "blocks",
    "tools": [
        "http_request"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
