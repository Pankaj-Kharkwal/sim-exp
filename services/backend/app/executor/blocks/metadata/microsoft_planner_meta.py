"""
Microsoft Planner Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "microsoft_planner",
    "name": "Microsoft Planner",
    "description": "Read and create tasks in Microsoft Planner",
    "long_description": """Integrate Microsoft Planner into the workflow. Can read and create tasks.""",
    "category": "tools",
    "tools": [
        "microsoft_planner_read_task",
        "microsoft_planner_create_task"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
