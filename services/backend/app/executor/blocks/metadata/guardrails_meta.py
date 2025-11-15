"""
Guardrails Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "guardrails",
    "name": "Guardrails",
    "description": "Validate content with guardrails",
    "long_description": """Validate content using guardrails. Check if content is valid JSON, matches a regex pattern, detect hallucinations using RAG + LLM scoring, or detect PII.""",
    "category": "blocks",
    "tools": [
        "guardrails_validate"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
