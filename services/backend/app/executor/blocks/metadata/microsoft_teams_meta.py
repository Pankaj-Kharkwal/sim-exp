"""
Microsoft Teams Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "microsoft_teams",
    "name": "Microsoft Teams",
    "description": "Read, write, and create messages",
    "long_description": """Integrate Microsoft Teams into the workflow. Can read and write chat messages, and read and write channel messages. Can be used in trigger mode to trigger a workflow when a message is sent to a chat or channel.""",
    "category": "tools",
    "tools": [
        "microsoft_teams_read_chat",
        "microsoft_teams_write_chat",
        "microsoft_teams_read_channel",
        "microsoft_teams_write_channel"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
