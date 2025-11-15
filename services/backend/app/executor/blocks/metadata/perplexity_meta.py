"""
Perplexity Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "perplexity",
    "name": "Perplexity",
    "description": "Use Perplexity AI chat models",
    "long_description": """Integrate Perplexity into the workflow. Can generate completions using Perplexity AI chat models.""",
    "category": "tools",
    "tools": [
        "perplexity_chat"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
