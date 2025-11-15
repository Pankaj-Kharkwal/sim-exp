"""
PostgreSQL Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "postgresql",
    "name": "PostgreSQL",
    "description": "Connect to PostgreSQL database",
    "long_description": """Integrate PostgreSQL into the workflow. Can query, insert, update, delete, and execute raw SQL.""",
    "category": "tools",
    "tools": [
        "postgresql_query",
        "postgresql_insert",
        "postgresql_update",
        "postgresql_delete",
        "postgresql_execute"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
