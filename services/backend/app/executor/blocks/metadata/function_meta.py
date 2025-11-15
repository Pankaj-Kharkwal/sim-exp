"""
Function Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "function",
    "name": "Function",
    "description": "Run custom logic",
    "long_description": """This is a core workflow block. Execute custom JavaScript or Python code within your workflow. Use E2B for remote execution with imports or enable Fast Mode (bolt) to run JavaScript locally for lowest latency.""",
    "category": "blocks",
    "tools": [
        "function_execute"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
