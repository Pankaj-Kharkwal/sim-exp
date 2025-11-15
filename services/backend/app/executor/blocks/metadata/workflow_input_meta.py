"""
Workflow Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "workflow_input",
    "name": "Workflow",
    "description": "Execute another workflow and map variables to its Input Form Trigger schema.",
    "long_description": """""",
    "category": "blocks",
    "tools": [
        "workflow_executor"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
