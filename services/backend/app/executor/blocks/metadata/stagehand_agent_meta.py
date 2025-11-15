"""
Stagehand Agent Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "stagehand_agent",
    "name": "Stagehand Agent",
    "description": "Autonomous web browsing agent",
    "long_description": """Integrate Stagehand Agent into the workflow. Can navigate the web and perform tasks.""",
    "category": "tools",
    "tools": [
        "stagehand_agent"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
