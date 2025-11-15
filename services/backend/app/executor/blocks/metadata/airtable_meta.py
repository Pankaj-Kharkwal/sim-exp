"""
Airtable Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "airtable",
    "name": "Airtable",
    "description": "Read, create, and update Airtable",
    "long_description": """Integrates Airtable into the workflow. Can create, get, list, or update Airtable records. Can be used in trigger mode to trigger a workflow when an update is made to an Airtable table.""",
    "category": "tools",
    "tools": [
        "airtable_list_records",
        "airtable_get_record",
        "airtable_create_records",
        "airtable_update_record",
        "airtable_update_multiple_records"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
