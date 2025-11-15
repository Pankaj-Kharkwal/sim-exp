"""
API Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "api_trigger",
    "name": "API",
    "description": "Expose as HTTP API endpoint",
    "long_description": """API trigger to start the workflow via authenticated HTTP calls with structured input.""",
    "category": "triggers",
    "tools": [],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
