"""
Agent Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "agent",
    "name": "Agent",
    "description": "Build an agent",
    "long_description": """The Agent block is a core workflow block that is a wrapper around an LLM. It takes in system/user prompts and calls an LLM provider. It can also make tool calls by directly containing tools inside of its tool input. It can additionally return structured output.""",
    "category": "blocks",
    "tools": [
        "openai_chat",
        "anthropic_chat",
        "google_chat",
        "xai_chat",
        "deepseek_chat",
        "deepseek_reasoner"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
