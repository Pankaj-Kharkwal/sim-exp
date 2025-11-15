"""
Hunter io Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "hunter",
    "name": "Hunter io",
    "description": "Find and verify professional email addresses",
    "long_description": """Integrate Hunter into the workflow. Can search domains, find email addresses, verify email addresses, discover companies, find companies, and count email addresses.""",
    "category": "tools",
    "tools": [
        "hunter_discover",
        "hunter_domain_search",
        "hunter_email_finder",
        "hunter_email_verifier",
        "hunter_companies_find",
        "hunter_email_count"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
