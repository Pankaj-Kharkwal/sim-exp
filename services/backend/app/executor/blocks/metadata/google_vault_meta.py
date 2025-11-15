"""
Google Vault Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "google_vault",
    "name": "Google Vault",
    "description": "Search, export, and manage holds/exports for Vault matters",
    "long_description": """Connect Google Vault to create exports, list exports, and manage holds within matters.""",
    "category": "tools",
    "tools": [
        "google_vault_create_matters_export",
        "google_vault_list_matters_export",
        "google_vault_download_export_file",
        "google_vault_create_matters_holds",
        "google_vault_list_matters_holds",
        "google_vault_create_matters",
        "google_vault_list_matters"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
