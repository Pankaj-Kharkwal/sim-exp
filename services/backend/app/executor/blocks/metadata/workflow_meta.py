"""
Workflow Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "workflow",
    "name": "Workflow",
    "description": "This is a core workflow block. Execute another workflow as a block in your workflow. Enter the input variable to pass to the child workflow.",
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
