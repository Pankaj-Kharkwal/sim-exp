"""
Resend Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "resend",
    "name": "Resend",
    "description": "Send emails with Resend.",
    "long_description": """Integrate Resend into the workflow. Can send emails. Requires API Key.""",
    "category": "tools",
    "tools": [
        "resend_send"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
