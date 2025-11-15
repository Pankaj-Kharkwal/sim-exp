"""Workflow management endpoints"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.core.auth import get_current_user
from app.db.session import get_db
from app.db.models.user import User
from app.db.models.organization import OrganizationMember
from sqlalchemy import select
from app.schemas.workflow import (
    WorkflowCreate,
    WorkflowUpdate,
    WorkflowResponse,
    WorkflowListResponse,
    WorkflowExecuteRequest,
    WorkflowExecuteResponse,
    WorkflowValidationResponse,
    WorkflowRead,
    WorkflowBlockSchema,
    WorkflowEdgeSchema,
)
from app.services.workflow_service import WorkflowService
from app.services.workflow_execution import WorkflowExecutionService
from app.db.models.workflow import Workflow as WorkflowModel, WorkflowBlock, WorkflowEdge


def _serialize_block(block: WorkflowBlock) -> WorkflowBlockSchema:
    """Convert DB block to API schema"""
    return WorkflowBlockSchema(
        id=block.id,
        type=block.type,
        name=block.name,
        position={"x": float(block.position_x), "y": float(block.position_y)},
        enabled=block.enabled,
        horizontal_handles=block.horizontal_handles,
        is_wide=block.is_wide,
        advanced_mode=block.advanced_mode,
        trigger_mode=block.trigger_mode,
        height=float(block.height or 0),
        sub_blocks=block.sub_blocks or {},
        outputs=block.outputs or {},
        data=block.data or {},
    )


def _serialize_edge(edge: WorkflowEdge) -> WorkflowEdgeSchema:
    """Convert DB edge to API schema"""
    return WorkflowEdgeSchema(
        id=edge.id,
        source=edge.source_block_id,
        target=edge.target_block_id,
        source_handle=edge.source_handle,
        target_handle=edge.target_handle,
        type=None,
        data=None,
    )


def _serialize_workflow(workflow: WorkflowModel) -> WorkflowRead:
    """Convert DB workflow to API schema"""
    return WorkflowRead(
        id=workflow.id,
        name=workflow.name,
        description=workflow.description,
        color=workflow.color,
        variables=workflow.variables or {},
        user_id=workflow.user_id,
        organization_id=workflow.organization_id,
        workspace_id=workflow.workspace_id,
        folder_id=workflow.folder_id,
        is_deployed=workflow.is_deployed,
        deployed_at=workflow.deployed_at,
        needs_redeployment=False,
        run_count=workflow.run_count,
        last_run_at=workflow.last_run_at,
        last_saved=None,
        created_at=workflow.created_at,
        updated_at=workflow.updated_at,
        blocks=[_serialize_block(b) for b in (workflow.blocks or [])],
        edges=[_serialize_edge(e) for e in (workflow.edges or [])],
        loops={},
        parallels={},
        deployment_statuses=None,
    )

router = APIRouter()
logger = get_logger(__name__)


async def get_user_organization_id(user_id: str, db: AsyncSession) -> Optional[str]:
    """Get the user's first organization ID"""
    query = select(OrganizationMember.organization_id).where(
        OrganizationMember.user_id == user_id
    ).limit(1)
    result = await db.execute(query)
    org_id = result.scalar_one_or_none()
    return org_id


@router.get("/", response_model=WorkflowListResponse)
async def list_workflows(
    skip: int = 0,
    limit: int = 100,
    include_public: bool = True,
    user_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    List all workflows

    - **skip**: Number of workflows to skip (pagination)
    - **limit**: Maximum number of workflows to return
    - **include_public**: Include public workflows
    - **user_id**: Filter by user ID (optional)
    """
    logger.info("list_workflows", skip=skip, limit=limit)

    service = WorkflowService()

    # Use current user if not specified
    if not user_id:
        user_id = current_user.id

    workflows, total = await service.list_workflows(
        user_id=user_id,
        skip=skip,
        limit=limit,
        include_public=include_public,
        db=db,
    )

    serialized = [_serialize_workflow(w) for w in workflows]
    page = (skip // limit) + 1 if limit else 1

    return WorkflowListResponse(
        workflows=serialized,
        total=total,
        page=page,
        page_size=limit,
    )


@router.post("/", response_model=WorkflowResponse, status_code=status.HTTP_201_CREATED)
async def create_workflow(
    workflow_data: WorkflowCreate = Body(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new workflow

    Example:
    ```json
    {
      "name": "My Workflow",
      "description": "A sample workflow",
      "blocks": [
        {
          "id": "block-1",
          "type": "agent",
          "label": "AI Agent",
          "data": {
            "model": "gpt-4",
            "prompt": "Hello"
          },
          "position": {"x": 0, "y": 0}
        }
      ],
      "edges": []
    }
    ```
    """
    logger.info("create_workflow", name=workflow_data.name)

    # Get user's organization
    org_id = await get_user_organization_id(current_user.id, db)
    if not org_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must belong to an organization to create workflows. Please create an organization first."
        )

    service = WorkflowService()

    workflow = await service.create_workflow(
        user_id=current_user.id,
        organization_id=org_id,
        workflow_data=workflow_data,
        db=db,
    )

    # Fetch with blocks and edges
    workflow = await service.get_workflow(
        workflow.id, db, include_blocks=True, include_edges=True
    )

    return WorkflowResponse(workflow=_serialize_workflow(workflow))


@router.get("/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow(
    workflow_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Get workflow by ID with full details"""
    logger.info("get_workflow", workflow_id=workflow_id)

    service = WorkflowService()
    workflow = await service.get_workflow(
        workflow_id, db, include_blocks=True, include_edges=True
    )

    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workflow not found: {workflow_id}",
        )

    return WorkflowResponse(workflow=_serialize_workflow(workflow))


@router.put("/{workflow_id}", response_model=WorkflowResponse)
async def update_workflow(
    workflow_id: str,
    workflow_data: WorkflowUpdate = Body(...),
    db: AsyncSession = Depends(get_db),
):
    """
    Update workflow

    Updates can include:
    - Name and description
    - Full blocks and edges replacement
    - Partial updates (only changed fields)
    """
    logger.info("update_workflow", workflow_id=workflow_id)

    service = WorkflowService()
    workflow = await service.update_workflow(workflow_id, workflow_data, db)

    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workflow not found: {workflow_id}",
        )

    # Refresh with blocks and edges
    workflow = await service.get_workflow(
        workflow_id, db, include_blocks=True, include_edges=True
    )

    return WorkflowResponse(workflow=_serialize_workflow(workflow))


@router.delete("/{workflow_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workflow(
    workflow_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Delete workflow and all related data"""
    logger.info("delete_workflow", workflow_id=workflow_id)

    service = WorkflowService()
    success = await service.delete_workflow(workflow_id, db)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workflow not found: {workflow_id}",
        )

    return None


@router.post("/{workflow_id}/validate", response_model=WorkflowValidationResponse)
async def validate_workflow(
    workflow_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Validate workflow structure

    Checks for:
    - Workflow exists
    - Has blocks
    - Disconnected blocks
    - Valid block types
    - No circular dependencies
    """
    logger.info("validate_workflow", workflow_id=workflow_id)

    service = WorkflowService()
    validation = await service.validate_workflow(workflow_id, db)

    return WorkflowValidationResponse(**validation)


@router.post("/{workflow_id}/snapshot")
async def create_snapshot(
    workflow_id: str,
    description: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """Create a snapshot of the workflow for versioning"""
    logger.info("create_snapshot", workflow_id=workflow_id)

    service = WorkflowService()
    snapshot = await service.create_snapshot(workflow_id, db, description)

    if not snapshot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workflow not found: {workflow_id}",
        )

    return {
        "id": snapshot.id,
        "workflow_id": snapshot.workflow_id,
        "version": snapshot.version,
        "description": snapshot.description,
        "created_at": snapshot.created_at,
    }


@router.post("/{workflow_id}/deploy")
async def deploy_workflow(
    workflow_id: str,
    snapshot_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """
    Deploy a workflow (create or use snapshot)

    If snapshot_id is not provided, a new snapshot will be created automatically.
    """
    logger.info("deploy_workflow", workflow_id=workflow_id, snapshot_id=snapshot_id)

    service = WorkflowService()
    deployment = await service.deploy_workflow(workflow_id, snapshot_id, db)

    if not deployment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workflow or snapshot not found",
        )

    return {
        "deployment_id": deployment.id,
        "workflow_id": deployment.workflow_id,
        "snapshot_id": deployment.snapshot_id,
        "status": deployment.status,
        "deployed_at": deployment.deployed_at,
    }


@router.post("/{workflow_id}/execute", response_model=WorkflowExecuteResponse)
async def execute_workflow(
    workflow_id: str,
    execute_request: WorkflowExecuteRequest = Body(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Execute a workflow

    Example:
    ```json
    {
      "input": {
        "user_message": "Hello, world!"
      },
      "workflow_trigger_type": "manual",
      "stream": false
    }
    ```
    """
    logger.info("execute_workflow_requested", workflow_id=workflow_id)

    execution_service = WorkflowExecutionService()
    response = await execution_service.execute_workflow(
        workflow_id=workflow_id,
        user_id=current_user.id,
        execute_request=execute_request,
        db=db,
    )

    return response
