"""
Manual Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "manual_trigger",
    "name": "Manual",
    "description": "Start workflow manually from the editor",
    "long_description": """Trigger the workflow manually without defining an input schema. Useful for simple runs where no structured input is needed.""",
    "category": "triggers",
    "tools": [],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
