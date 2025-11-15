"""
API endpoints for workflow blocks
Provides block metadata and registry info to frontend
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

from app.core.logging import get_logger
from app.executor.blocks.registry import get_all_blocks, get_block_metadata

logger = get_logger(__name__)

router = APIRouter(prefix="/blocks", tags=["Blocks"])


@router.get("/", response_model=List[Dict[str, Any]])
async def list_all_blocks():
    """
    Get all available workflow blocks with their metadata

    Returns:
        List of block metadata objects
    """
    try:
        blocks = get_all_blocks()
        logger.info("blocks_listed", count=len(blocks))
        return blocks
    except Exception as e:
        logger.error("failed_to_list_blocks", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve blocks")


@router.get("/{block_type}", response_model=Dict[str, Any])
async def get_block(block_type: str):
    """
    Get metadata for a specific block type

    Args:
        block_type: The type identifier of the block

    Returns:
        Block metadata object
    """
    try:
        block = get_block_metadata(block_type)

        if not block:
            raise HTTPException(
                status_code=404,
                detail=f"Block type '{block_type}' not found"
            )

        logger.info("block_retrieved", block_type=block_type)
        return block

    except HTTPException:
        raise
    except Exception as e:
        logger.error("failed_to_get_block", block_type=block_type, error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve block")


@router.get("/category/{category}", response_model=List[Dict[str, Any]])
async def get_blocks_by_category(category: str):
    """
    Get blocks filtered by category

    Args:
        category: Category name (e.g., 'blocks', 'integrations', 'triggers')

    Returns:
        List of block metadata objects in that category
    """
    try:
        from app.executor.blocks.registry import registry
        blocks = registry.get_blocks_by_category(category)

        logger.info("blocks_by_category_retrieved", category=category, count=len(blocks))
        return blocks

    except Exception as e:
        logger.error("failed_to_get_blocks_by_category", category=category, error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve blocks by category")
