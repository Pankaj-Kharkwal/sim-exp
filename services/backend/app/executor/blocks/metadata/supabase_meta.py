"""
Supabase Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "supabase",
    "name": "Supabase",
    "description": "Use Supabase database",
    "long_description": """Integrate Supabase into the workflow. Can get many rows, get, create, update, delete, and upsert a row.""",
    "category": "tools",
    "tools": [
        "supabase_query",
        "supabase_insert",
        "supabase_get_row",
        "supabase_update",
        "supabase_delete",
        "supabase_upsert",
        "supabase_vector_search"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
