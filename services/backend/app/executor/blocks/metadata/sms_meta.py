"""
SMS Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "sms",
    "name": "SMS",
    "description": "Send SMS messages using the internal SMS service",
    "long_description": """Send SMS messages directly using the internal SMS service powered by Twilio. No external configuration or OAuth required. Perfect for sending notifications, alerts, or general purpose text messages from your workflows. Requires valid phone numbers with country codes.""",
    "category": "tools",
    "tools": [
        "sms_send"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
