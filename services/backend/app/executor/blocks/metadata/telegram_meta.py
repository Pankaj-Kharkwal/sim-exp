"""
Telegram Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "telegram",
    "name": "Telegram",
    "description": "Interact with Telegram",
    "long_description": """Integrate Telegram into the workflow. Can send and delete messages. Can be used in trigger mode to trigger a workflow when a message is sent to a chat.""",
    "category": "tools",
    "tools": [
        "telegram_message",
        "telegram_delete_message",
        "telegram_send_photo",
        "telegram_send_video",
        "telegram_send_audio",
        "telegram_send_animation",
        "telegram_send_document"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
