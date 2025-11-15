"""
Google Forms Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "google_forms",
    "name": "Google Forms",
    "description": "Read responses from a Google Form",
    "long_description": """Integrate Google Forms into your workflow. Provide a Form ID to list responses, or specify a Response ID to fetch a single response. Requires OAuth.""",
    "category": "tools",
    "tools": [
        "google_forms_get_responses"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
