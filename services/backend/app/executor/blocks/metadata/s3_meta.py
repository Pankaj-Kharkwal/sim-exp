"""
S3 Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "s3",
    "name": "S3",
    "description": "Upload, download, list, and manage S3 files",
    "long_description": """Integrate S3 into the workflow. Upload files, download objects, list bucket contents, delete objects, and copy objects between buckets. Requires AWS access key and secret access key.""",
    "category": "tools",
    "tools": [
        "s3_put_object",
        "s3_get_object",
        "s3_list_objects",
        "s3_delete_object",
        "s3_copy_object"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
