"""
Input Form Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "input_trigger",
    "name": "Input Form",
    "description": "Start workflow manually with a defined input schema",
    "long_description": """Manually trigger the workflow from the editor with a structured input schema. This enables typed inputs for parent workflows to map into.""",
    "category": "triggers",
    "tools": [],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
