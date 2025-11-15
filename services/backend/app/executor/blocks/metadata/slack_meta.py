"""
Slack Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "slack",
    "name": "Slack",
    "description": "Send messages to Slack or trigger workflows from Slack events",
    "long_description": """Integrate Slack into the workflow. Can send messages, create canvases, and read messages. Requires Bot Token instead of OAuth in advanced mode. Can be used in trigger mode to trigger a workflow when a message is sent to a channel.""",
    "category": "tools",
    "tools": [
        "slack_message",
        "slack_canvas",
        "slack_message_reader"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
