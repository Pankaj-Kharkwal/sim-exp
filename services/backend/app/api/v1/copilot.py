"""Copilot API endpoints - AI-assisted workflow building"""

from typing import Optional, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field

from app.core.auth import get_current_user
from app.core.logging import get_logger
from app.db.models.user import User
from app.db.session import get_db
from app.services.copilot_service import copilot_service

logger = get_logger(__name__)

router = APIRouter(prefix="/copilot", tags=["Copilot"])


# Schemas
class CopilotRequest(BaseModel):
    """Copilot request schema"""
    prompt: str = Field(..., description="User prompt for copilot")
    workflow_id: Optional[str] = Field(None, alias="workflowId")
    context: Optional[dict[str, Any]] = Field(default_factory=dict, description="Additional context")
    action: str = Field(default="suggest", description="Action: suggest, generate, explain, fix")

    model_config = {"populate_by_name": True}


class BlockSuggestion(BaseModel):
    """Block suggestion schema"""
    type: str
    name: str
    description: str
    suggested_data: dict[str, Any] = Field(alias="suggestedData")
    confidence: float = Field(ge=0.0, le=1.0)

    model_config = {"populate_by_name": True}


class CopilotResponse(BaseModel):
    """Copilot response schema"""
    suggestions: list[BlockSuggestion] = Field(default_factory=list)
    explanation: Optional[str] = None
    code: Optional[str] = None
    workflow_updates: Optional[dict[str, Any]] = Field(None, alias="workflowUpdates")

    model_config = {"populate_by_name": True}


class GenerateBlockRequest(BaseModel):
    """Generate AI block request"""
    description: str = Field(..., description="Description of what the block should do")
    inputs: Optional[list[str]] = Field(default_factory=list)
    outputs: Optional[list[str]] = Field(default_factory=list)
    language: str = Field(default="python", description="Programming language")

    model_config = {"populate_by_name": True}


class GeneratedBlock(BaseModel):
    """Generated block response"""
    type: str = "custom_code"
    name: str
    description: str
    code: str
    inputs: list[dict[str, Any]]
    outputs: list[dict[str, Any]]
    test_cases: Optional[list[dict[str, Any]]] = Field(None, alias="testCases")

    model_config = {"populate_by_name": True}


# Endpoints
@router.post("/suggest", response_model=CopilotResponse)
async def get_copilot_suggestions(
    request: CopilotRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get AI-powered suggestions for workflow building

    This endpoint provides:
    - Block suggestions based on user intent
    - Workflow improvements
    - Connection suggestions
    - Best practices recommendations
    """
    logger.info(
        "copilot_suggestion_requested",
        user_id=current_user.id,
        workflow_id=request.workflow_id,
        action=request.action,
    )

    result = await copilot_service.get_suggestions(
        prompt=request.prompt,
        workflow_id=request.workflow_id,
        action=request.action,
        db=db,
    )

    return CopilotResponse(**result)


@router.post("/generate-block", response_model=GeneratedBlock)
async def generate_custom_block(
    request: GenerateBlockRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Generate a custom block using AI

    Creates a new custom block based on natural language description.
    The AI will:
    - Generate the block code
    - Define inputs and outputs
    - Create test cases
    - Provide documentation
    """
    logger.info(
        "block_generation_requested",
        user_id=current_user.id,
        language=request.language,
    )

    block = await copilot_service.generate_custom_block(
        description=request.description,
        inputs=request.inputs or [],
        outputs=request.outputs or [],
        language=request.language,
    )

    return GeneratedBlock(**block)


@router.post("/explain")
async def explain_workflow(
    workflow_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get AI explanation of a workflow

    Provides human-readable explanation of:
    - What the workflow does
    - How it works step-by-step
    - Potential issues or improvements
    """
    logger.info(
        "workflow_explanation_requested",
        user_id=current_user.id,
        workflow_id=workflow_id,
    )

    try:
        explanation = await copilot_service.explain_workflow(workflow_id, db)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return explanation


@router.post("/fix")
async def fix_workflow_errors(
    workflow_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get AI-powered fixes for workflow errors

    Analyzes workflow errors and suggests fixes:
    - Missing connections
    - Configuration errors
    - Logic issues
    - Performance optimizations
    """
    logger.info(
        "workflow_fix_requested",
        user_id=current_user.id,
        workflow_id=workflow_id,
    )

    try:
        report = await copilot_service.fix_workflow_errors(workflow_id, db)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return report
