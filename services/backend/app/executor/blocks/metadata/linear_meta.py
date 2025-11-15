"""
Linear Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "linear",
    "name": "Linear",
    "description": "Read and create issues in Linear",
    "long_description": """Integrate Linear into the workflow. Can read and create issues.""",
    "category": "tools",
    "tools": [
        "linear_read_issues",
        "linear_create_issue"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
