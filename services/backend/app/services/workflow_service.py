"""
Workflow Service - Complete CRUD operations for workflows

Handles:
- Workflow creation, reading, updating, deletion
- Block management within workflows
- Edge/connection management
- Workflow versioning and deployment
- Workflow validation
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid
import json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, and_, or_
from sqlalchemy.orm import selectinload

from app.core.logging import get_logger
from app.db.models.workflow import (
    Workflow,
    WorkflowBlock,
    WorkflowEdge,
    WorkflowExecutionSnapshot,
)
from app.schemas.workflow import (
    WorkflowCreate,
    WorkflowUpdate,
    WorkflowResponse,
)

logger = get_logger(__name__)


def _to_dict(payload: Any) -> Dict[str, Any]:
    """Convert Pydantic models (or plain dicts) into standard dictionaries."""
    if hasattr(payload, "model_dump"):
        return payload.model_dump(by_alias=True)  # type: ignore[attr-defined]
    return payload


class WorkflowService:
    """Service for workflow management operations"""

    async def create_workflow(
        self,
        user_id: str,
        organization_id: str,
        workflow_data: WorkflowCreate,
        db: AsyncSession,
    ) -> Workflow:
        """Create a new workflow"""

        logger.info(
            "workflow_create_requested",
            name=workflow_data.name,
            user_id=user_id,
        )

        now = datetime.utcnow()

        # Create workflow
        workflow = Workflow(
            id=str(uuid.uuid4()),
            name=workflow_data.name,
            description=workflow_data.description,
            user_id=user_id,
            organization_id=organization_id,
            workspace_id=workflow_data.workspace_id,
            folder_id=workflow_data.folder_id,
            last_synced=now,
            is_published=workflow_data.is_published or False,
            created_at=now,
            updated_at=now,
        )

        db.add(workflow)
        await db.flush()

        # Create blocks if provided
        if workflow_data.blocks:
            now = datetime.utcnow()
            for block_data in workflow_data.blocks:
                block_dict = _to_dict(block_data)
                position = block_dict.get("position") or {}
                data_payload = block_dict.get("data") or {}
                block = WorkflowBlock(
                    id=block_dict.get("id") or str(uuid.uuid4()),
                    workflow_id=workflow.id,
                    type=block_dict["type"],
                    name=block_dict.get("name")
                    or block_dict.get("label")
                    or block_dict["type"].title(),
                    position_x=position.get("x", 0),
                    position_y=position.get("y", 0),
                    enabled=block_dict.get("enabled", True),
                    horizontal_handles=block_dict.get("horizontalHandles")
                    if "horizontalHandles" in block_dict
                    else block_dict.get("horizontal_handles", True),
                    is_wide=block_dict.get("isWide")
                    if "isWide" in block_dict
                    else block_dict.get("is_wide", False),
                    advanced_mode=block_dict.get("advancedMode")
                    if "advancedMode" in block_dict
                    else block_dict.get("advanced_mode", False),
                    trigger_mode=block_dict.get("triggerMode")
                    if "triggerMode" in block_dict
                    else block_dict.get("trigger_mode", False),
                    height=block_dict.get("height", 0),
                    sub_blocks=block_dict.get("subBlocks")
                    if "subBlocks" in block_dict
                    else block_dict.get("sub_blocks", {}),
                    outputs=block_dict.get("outputs", {}),
                    data=data_payload or {},
                    created_at=now,
                    updated_at=now,
                )
                db.add(block)

        # Create edges if provided
        if workflow_data.edges:
            for edge_data in workflow_data.edges:
                edge_dict = _to_dict(edge_data)
                edge = WorkflowEdge(
                    id=edge_dict.get("id") or str(uuid.uuid4()),
                    workflow_id=workflow.id,
                    source_block_id=edge_dict["source"],
                    target_block_id=edge_dict["target"],
                    source_handle=edge_dict.get("sourceHandle"),
                    target_handle=edge_dict.get("targetHandle"),
                    created_at=datetime.utcnow(),
                )
                db.add(edge)

        await db.commit()
        await db.refresh(workflow)

        logger.info(
            "workflow_created",
            workflow_id=workflow.id,
            name=workflow.name,
            blocks_count=len(workflow_data.blocks or []),
            edges_count=len(workflow_data.edges or []),
        )

        return workflow

    async def get_workflow(
        self,
        workflow_id: str,
        db: AsyncSession,
        include_blocks: bool = True,
        include_edges: bool = True,
    ) -> Optional[Workflow]:
        """Get workflow by ID with optional relationships"""

        query = select(Workflow).where(Workflow.id == workflow_id)

        if include_blocks:
            query = query.options(selectinload(Workflow.blocks))

        if include_edges:
            query = query.options(selectinload(Workflow.edges))

        result = await db.execute(query)
        workflow = result.scalar_one_or_none()

        if workflow:
            logger.debug(
                "workflow_retrieved",
                workflow_id=workflow_id,
                name=workflow.name,
            )

        return workflow

    async def list_workflows(
        self,
        user_id: Optional[str] = None,
        organization_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
        include_public: bool = True,
        db: AsyncSession = None,
    ) -> tuple[List[Workflow], int]:
        """List workflows with filtering"""

        # Build query with eager loading of relationships
        query = select(Workflow).options(
            selectinload(Workflow.blocks),
            selectinload(Workflow.edges)
        )

        # Build base filters for user/org ownership
        base_filters = []
        if user_id:
            base_filters.append(Workflow.user_id == user_id)
        if organization_id:
            base_filters.append(Workflow.organization_id == organization_id)

        # Apply filters with OR logic for public workflows
        if base_filters and include_public:
            # Show workflows owned by user/org OR published workflows
            where_clause = or_(and_(*base_filters), Workflow.is_published == True)
            query = query.where(where_clause)
        elif base_filters:
            # Only user/org workflows
            where_clause = and_(*base_filters)
            query = query.where(where_clause)
        elif include_public:
            # Only published workflows
            where_clause = Workflow.is_published == True
            query = query.where(where_clause)
        else:
            where_clause = None

        # Get total count using the same where clause
        from sqlalchemy import func
        if where_clause is not None:
            count_query = select(func.count(Workflow.id)).where(where_clause)
        else:
            count_query = select(func.count(Workflow.id))
        count_result = await db.execute(count_query)
        total = count_result.scalar() or 0

        # Apply pagination
        query = query.offset(skip).limit(limit)
        query = query.order_by(Workflow.updated_at.desc())

        result = await db.execute(query)
        workflows = result.scalars().all()

        logger.info(
            "workflows_listed",
            count=len(workflows),
            total=total,
            user_id=user_id,
        )

        return list(workflows), total

    async def update_workflow(
        self,
        workflow_id: str,
        workflow_data: WorkflowUpdate,
        db: AsyncSession,
    ) -> Optional[Workflow]:
        """Update workflow"""

        # Fetch workflow
        workflow = await self.get_workflow(
            workflow_id, db, include_blocks=True, include_edges=True
        )

        if not workflow:
            logger.warning("workflow_not_found", workflow_id=workflow_id)
            return None

        logger.info(
            "workflow_update_requested",
            workflow_id=workflow_id,
            fields=list(workflow_data.dict(exclude_unset=True).keys()),
        )

        # Update basic fields
        if workflow_data.name is not None:
            workflow.name = workflow_data.name
        if workflow_data.description is not None:
            workflow.description = workflow_data.description
        if workflow_data.is_published is not None:
            workflow.is_published = workflow_data.is_published

        # Update blocks if provided
        if workflow_data.blocks is not None:
            # Delete existing blocks
            await db.execute(
                delete(WorkflowBlock).where(WorkflowBlock.workflow_id == workflow_id)
            )

            # Create new blocks
            now = datetime.utcnow()
            for block_data in workflow_data.blocks:
                block_dict = _to_dict(block_data)
                position = block_dict.get("position") or {}
                data_payload = block_dict.get("data") or {}
                block = WorkflowBlock(
                    id=block_dict.get("id") or str(uuid.uuid4()),
                    workflow_id=workflow.id,
                    type=block_dict["type"],
                    name=block_dict.get("name")
                    or block_dict.get("label")
                    or block_dict["type"].title(),
                    position_x=position.get("x", 0),
                    position_y=position.get("y", 0),
                    enabled=block_dict.get("enabled", True),
                    horizontal_handles=block_dict.get("horizontalHandles")
                    if "horizontalHandles" in block_dict
                    else block_dict.get("horizontal_handles", True),
                    is_wide=block_dict.get("isWide")
                    if "isWide" in block_dict
                    else block_dict.get("is_wide", False),
                    advanced_mode=block_dict.get("advancedMode")
                    if "advancedMode" in block_dict
                    else block_dict.get("advanced_mode", False),
                    trigger_mode=block_dict.get("triggerMode")
                    if "triggerMode" in block_dict
                    else block_dict.get("trigger_mode", False),
                    height=block_dict.get("height", 0),
                    sub_blocks=block_dict.get("subBlocks")
                    if "subBlocks" in block_dict
                    else block_dict.get("sub_blocks", {}),
                    outputs=block_dict.get("outputs", {}),
                    data=data_payload or {},
                    created_at=now,
                    updated_at=now,
                )
                db.add(block)

        # Update edges if provided
        if workflow_data.edges is not None:
            # Delete existing edges
            await db.execute(
                delete(WorkflowEdge).where(WorkflowEdge.workflow_id == workflow_id)
            )

            # Create new edges
            for edge_data in workflow_data.edges:
                edge_dict = _to_dict(edge_data)
                edge = WorkflowEdge(
                    id=edge_dict.get("id") or str(uuid.uuid4()),
                    workflow_id=workflow.id,
                    source_block_id=edge_dict["source"],
                    target_block_id=edge_dict["target"],
                    source_handle=edge_dict.get("sourceHandle"),
                    target_handle=edge_dict.get("targetHandle"),
                    created_at=datetime.utcnow(),
                )
                db.add(edge)

        # Update timestamp
        workflow.updated_at = datetime.utcnow()

        await db.commit()
        await db.refresh(workflow)

        logger.info(
            "workflow_updated",
            workflow_id=workflow_id,
            blocks_count=len(workflow_data.blocks or []),
            edges_count=len(workflow_data.edges or []),
        )

        return workflow

    async def delete_workflow(
        self,
        workflow_id: str,
        db: AsyncSession,
    ) -> bool:
        """Delete workflow and all related data"""

        logger.info("workflow_delete_requested", workflow_id=workflow_id)

        # Fetch workflow to confirm it exists
        workflow = await self.get_workflow(workflow_id, db, include_blocks=False, include_edges=False)

        if not workflow:
            logger.warning("workflow_not_found", workflow_id=workflow_id)
            return False

        # Delete edges first (foreign key constraints)
        await db.execute(delete(WorkflowEdge).where(WorkflowEdge.workflow_id == workflow_id))

        # Delete blocks
        await db.execute(delete(WorkflowBlock).where(WorkflowBlock.workflow_id == workflow_id))

        # Delete workflow
        await db.execute(delete(Workflow).where(Workflow.id == workflow_id))

        await db.commit()

        logger.info("workflow_deleted", workflow_id=workflow_id)

        return True

    async def create_snapshot(
        self,
        workflow_id: str,
        db: AsyncSession,
    ) -> Optional[WorkflowExecutionSnapshot]:
        """Create a snapshot of the workflow for execution tracking"""

        # Fetch workflow with blocks and edges
        workflow = await self.get_workflow(
            workflow_id, db, include_blocks=True, include_edges=True
        )

        if not workflow:
            return None

        logger.info("workflow_snapshot_creating", workflow_id=workflow_id)

        # Serialize workflow state
        snapshot_data = {
            "name": workflow.name,
            "description": workflow.description,
            "blocks": [
                {
                    "id": block.id,
                    "type": block.type,
                    "name": block.name,
                    "data": block.data,
                    "position": {"x": float(block.position_x), "y": float(block.position_y)},
                }
                for block in workflow.blocks
            ],
            "edges": [
                {
                    "id": edge.id,
                    "source": edge.source_block_id,
                    "target": edge.target_block_id,
                    "sourceHandle": edge.source_handle,
                    "targetHandle": edge.target_handle,
                }
                for edge in workflow.edges
            ],
        }

        # Create state hash
        import hashlib
        state_hash = hashlib.sha256(
            json.dumps(snapshot_data, sort_keys=True).encode()
        ).hexdigest()

        # Create snapshot
        snapshot = WorkflowExecutionSnapshot(
            id=str(uuid.uuid4()),
            workflow_id=workflow_id,
            state_hash=state_hash,
            state_data=snapshot_data,
        )

        db.add(snapshot)
        await db.commit()
        await db.refresh(snapshot)

        logger.info(
            "workflow_snapshot_created",
            workflow_id=workflow_id,
            snapshot_id=snapshot.id,
            state_hash=state_hash[:8],
        )

        return snapshot

    async def deploy_workflow(
        self,
        workflow_id: str,
        db: AsyncSession,
    ) -> Optional[Workflow]:
        """Deploy a workflow by saving current state"""

        # Fetch workflow
        workflow = await self.get_workflow(
            workflow_id, db, include_blocks=True, include_edges=True
        )

        if not workflow:
            return None

        # Create snapshot for deployment tracking
        snapshot = await self.create_snapshot(workflow_id, db)

        if not snapshot:
            return None

        logger.info(
            "workflow_deployment_creating",
            workflow_id=workflow_id,
            snapshot_id=snapshot.id,
        )

        # Update workflow with deployment state
        workflow.deployed_state = snapshot.state_data
        workflow.deployed_at = datetime.utcnow()
        workflow.is_deployed = True

        await db.commit()
        await db.refresh(workflow)

        logger.info(
            "workflow_deployment_created",
            workflow_id=workflow_id,
            snapshot_id=snapshot.id,
        )

        return workflow

    async def validate_workflow(
        self,
        workflow_id: str,
        db: AsyncSession,
    ) -> Dict[str, Any]:
        """Validate workflow structure"""

        workflow = await self.get_workflow(
            workflow_id, db, include_blocks=True, include_edges=True
        )

        if not workflow:
            return {
                "valid": False,
                "errors": ["Workflow not found"],
            }

        errors = []
        warnings = []

        # Check if workflow has blocks
        if not workflow.blocks:
            errors.append("Workflow has no blocks")

        # Check for disconnected blocks
        connected_blocks = set()
        for edge in workflow.edges:
            connected_blocks.add(edge.source_block_id)
            connected_blocks.add(edge.target_block_id)

        disconnected = [
            block.id for block in workflow.blocks if block.id not in connected_blocks
        ]
        if len(disconnected) > 1:  # More than 1 disconnected block is suspicious
            warnings.append(f"{len(disconnected)} blocks are not connected")

        # Check for circular dependencies (basic check)
        # TODO: Implement proper topological sort check

        # Check for valid block types
        # TODO: Validate against registered block types

        logger.info(
            "workflow_validated",
            workflow_id=workflow_id,
            valid=len(errors) == 0,
            errors_count=len(errors),
            warnings_count=len(warnings),
        )

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
        }
