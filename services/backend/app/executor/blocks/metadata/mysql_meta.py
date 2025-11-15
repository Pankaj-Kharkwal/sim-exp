"""
MySQL Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "mysql",
    "name": "MySQL",
    "description": "Connect to MySQL database",
    "long_description": """Integrate MySQL into the workflow. Can query, insert, update, delete, and execute raw SQL.""",
    "category": "tools",
    "tools": [
        "mysql_query",
        "mysql_insert",
        "mysql_update",
        "mysql_delete",
        "mysql_execute"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
