"""
Typeform Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "typeform",
    "name": "Typeform",
    "description": "Interact with Typeform",
    "long_description": """Integrate Typeform into the workflow. Can retrieve responses, download files, and get form insights. Requires API Key.""",
    "category": "tools",
    "tools": [
        "typeform_responses",
        "typeform_files",
        "typeform_insights"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
