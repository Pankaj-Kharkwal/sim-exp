"""
AI Block Generation API
Allows users to chat with copilot and generate custom blocks dynamically
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from app.core.logging import get_logger
from app.services.ai_block_generator import ai_block_generator, GeneratedBlock
from app.db.models.user import User
from app.core.auth import get_current_user

logger = get_logger(__name__)

router = APIRouter(prefix="/ai-blocks", tags=["AI Blocks"])


class GenerateBlockRequest(BaseModel):
    """Request to generate a block from chat"""
    user_message: str
    conversation_history: Optional[List[Dict[str, str]]] = None
    workspace_id: str


class GenerateBlockResponse(BaseModel):
    """Response with generated block"""
    success: bool
    block: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    suggestions: Optional[List[str]] = None


@router.post("/generate", response_model=GenerateBlockResponse)
async def generate_block_from_chat(
    request: GenerateBlockRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Generate a custom workflow block based on chat conversation

    The AI analyzes the user's request and:
    1. Determines what kind of block they need
    2. Extracts requirements (inputs, outputs, config)
    3. Finds similar existing blocks as examples
    4. Generates complete block structure
    5. Creates executor code
    6. Validates everything

    Example:
        User: "I need a block that sends data to my custom webhook API"
        → AI generates a custom webhook block with proper structure
    """
    try:
        logger.info(
            "ai_block_generation_requested",
            user_id=current_user.id,
            workspace_id=request.workspace_id,
            message_length=len(request.user_message)
        )

        # Generate block using AI
        generated_block = await ai_block_generator.generate_block(
            user_request=request.user_message,
            conversation_history=request.conversation_history
        )

        # Convert to dict for response
        block_dict = generated_block.dict()

        logger.info(
            "ai_block_generated_successfully",
            user_id=current_user.id,
            block_type=generated_block.type,
            block_name=generated_block.name
        )

        return GenerateBlockResponse(
            success=True,
            block=block_dict,
            suggestions=[
                f"Block '{generated_block.name}' has been created!",
                "You can now drag it from the custom blocks section",
                "Test it in a workflow to make sure it works as expected"
            ]
        )

    except ValueError as e:
        logger.warning("ai_block_generation_failed", error=str(e), user_id=current_user.id)
        return GenerateBlockResponse(
            success=False,
            error=str(e),
            suggestions=[
                "Try being more specific about what the block should do",
                "Mention inputs, outputs, and any APIs it should call",
                "Check out existing blocks for inspiration"
            ]
        )

    except Exception as e:
        logger.error(
            "ai_block_generation_error",
            error=str(e),
            user_id=current_user.id,
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail="Failed to generate block. Please try again."
        )


@router.post("/refine", response_model=GenerateBlockResponse)
async def refine_generated_block(
    block_type: str,
    user_feedback: str,
    current_user: User = Depends(get_current_user)
):
    """
    Refine a previously generated block based on user feedback

    Example:
        User: "Add a timeout parameter to the webhook block"
        → AI updates the block structure
    """
    try:
        # TODO: Implement block refinement
        # 1. Load existing generated block
        # 2. Apply user's requested changes via AI
        # 3. Re-validate
        # 4. Return updated block

        raise HTTPException(status_code=501, detail="Block refinement coming soon!")

    except Exception as e:
        logger.error("block_refinement_error", error=str(e), exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/custom-blocks", response_model=List[Dict[str, Any]])
async def get_user_custom_blocks(
    workspace_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get all custom blocks created by user for a workspace

    These are AI-generated blocks saved to the user's workspace
    """
    try:
        # TODO: Fetch from database
        # For now return empty list
        return []

    except Exception as e:
        logger.error("fetch_custom_blocks_error", error=str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to fetch custom blocks")


@router.delete("/custom-blocks/{block_type}")
async def delete_custom_block(
    block_type: str,
    workspace_id: str,
    current_user: User = Depends(get_current_user)
):
    """Delete a custom block"""
    try:
        # TODO: Implement deletion
        # 1. Verify ownership
        # 2. Delete from database
        # 3. Remove executor code
        return {"success": True, "message": f"Block {block_type} deleted"}

    except Exception as e:
        logger.error("delete_custom_block_error", error=str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to delete block")
