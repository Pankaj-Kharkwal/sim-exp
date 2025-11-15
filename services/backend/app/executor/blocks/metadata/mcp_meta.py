"""
MCP Tool Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "mcp",
    "name": "MCP Tool",
    "description": "Execute tools from Model Context Protocol (MCP) servers",
    "long_description": """Integrate MCP into the workflow. Can execute tools from MCP servers. Requires MCP servers in workspace settings.""",
    "category": "tools",
    "tools": [],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
