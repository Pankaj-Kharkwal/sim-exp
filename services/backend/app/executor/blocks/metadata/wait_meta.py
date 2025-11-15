"""
Wait Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "wait",
    "name": "Wait",
    "description": "Pause workflow execution for a specified time delay",
    "long_description": """Pauses workflow execution for a specified time interval. The wait executes a simple sleep for the configured duration.""",
    "category": "blocks",
    "tools": [],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
