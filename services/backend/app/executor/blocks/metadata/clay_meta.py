"""
Clay Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "clay",
    "name": "Clay",
    "description": "Populate Clay workbook",
    "long_description": """Integrate Clay into the workflow. Can populate a table with data.""",
    "category": "tools",
    "tools": [
        "clay_populate"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
