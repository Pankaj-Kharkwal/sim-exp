"""
GitHub Block Metadata
Auto-generated from TypeScript block config
"""

from typing import Dict, Any, List

BLOCK_METADATA = {
    "type": "github",
    "name": "GitHub",
    "description": "Interact with GitHub or trigger workflows from GitHub events",
    "long_description": """Integrate Github into the workflow. Can get get PR details, create PR comment, get repository info, and get latest commit. Can be used in trigger mode to trigger a workflow when a PR is created, commented on, or a commit is pushed.""",
    "category": "tools",
    "tools": [
        "github_pr",
        "github_comment",
        "github_repo_info",
        "github_latest_commit"
],
    "inputs": {},
    "outputs": {},
}


def get_block_metadata() -> Dict[str, Any]:
    """Get block metadata"""
    return BLOCK_METADATA
