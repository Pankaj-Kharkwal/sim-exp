"""
Variables Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "variables",
    "name": "Variables",
    "description": "Set workflow-scoped variables",
    "long_description": """Set workflow-scoped variables that can be accessed throughout the workflow using <variable.variableName> syntax. All Variables blocks share the same namespace, so later blocks can update previously set variables.""",
    "category": "blocks",
    "tools": [],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
