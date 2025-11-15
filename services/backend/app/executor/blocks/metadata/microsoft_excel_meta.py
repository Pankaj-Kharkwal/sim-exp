"""
Microsoft Excel Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "microsoft_excel",
    "name": "Microsoft Excel",
    "description": "Read, write, and update data",
    "long_description": """Integrate Microsoft Excel into the workflow. Can read, write, update, and add to table.""",
    "category": "tools",
    "tools": [
        "microsoft_excel_read",
        "microsoft_excel_write",
        "microsoft_excel_table_add"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
