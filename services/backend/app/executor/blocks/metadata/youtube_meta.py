"""
YouTube Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "youtube",
    "name": "YouTube",
    "description": "Interact with YouTube videos, channels, and playlists",
    "long_description": """Integrate YouTube into the workflow. Can search for videos, get video details, get channel information, get playlist items, and get video comments.""",
    "category": "tools",
    "tools": [
        "youtube_search",
        "youtube_video_details",
        "youtube_channel_info",
        "youtube_playlist_items",
        "youtube_comments"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
