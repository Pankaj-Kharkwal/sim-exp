"""
Twilio SMS Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "twilio_sms",
    "name": "Twilio SMS",
    "description": "Send SMS messages",
    "long_description": """Integrate Twilio into the workflow. Can send SMS messages.""",
    "category": "tools",
    "tools": [
        "twilio_send_sms"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
