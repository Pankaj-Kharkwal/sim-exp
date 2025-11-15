"""
Discord Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "discord",
    "name": "Discord",
    "description": "Interact with Discord",
    "long_description": """Integrate Discord into the workflow. Can send and get messages, get server information, and get a user’s information.""",
    "category": "tools",
    "tools": [
        "discord_send_message",
        "discord_get_messages",
        "discord_get_server",
        "discord_get_user"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
