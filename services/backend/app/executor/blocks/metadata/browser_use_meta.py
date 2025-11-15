"""
Browser Use Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "browser_use",
    "name": "Browser Use",
    "description": "Run browser automation tasks",
    "long_description": """Integrate Browser Use into the workflow. Can navigate the web and perform actions as if a real user was interacting with the browser.""",
    "category": "tools",
    "tools": [
        "browser_use_run_task"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
