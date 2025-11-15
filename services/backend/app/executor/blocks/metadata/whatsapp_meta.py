"""
WhatsApp Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "whatsapp",
    "name": "WhatsApp",
    "description": "Send WhatsApp messages",
    "long_description": """Integrate WhatsApp into the workflow. Can send messages.""",
    "category": "tools",
    "tools": [
        "whatsapp_send_message"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
