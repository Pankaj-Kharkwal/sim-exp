"""
ElevenLabs Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "elevenlabs",
    "name": "ElevenLabs",
    "description": "Convert TTS using ElevenLabs",
    "long_description": """Integrate ElevenLabs into the workflow. Can convert text to speech.""",
    "category": "tools",
    "tools": [
        "elevenlabs_tts"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
