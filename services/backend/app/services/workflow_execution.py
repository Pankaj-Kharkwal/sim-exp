"""Workflow execution service"""

from datetime import datetime
from typing import Any, Optional
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.logging import get_logger, set_trace_id
from app.db.models import Workflow, WorkflowExecutionLog, WorkflowExecutionSnapshot
from app.executor import WorkflowExecutor
from app.schemas.workflow import WorkflowExecuteRequest, WorkflowExecuteResponse

logger = get_logger(__name__)


class WorkflowExecutionService:
    """Service for workflow execution"""

    def __init__(self):
        self.executor = WorkflowExecutor()

    async def execute_workflow(
        self,
        workflow_id: str,
        user_id: str,
        execute_request: WorkflowExecuteRequest,
        db: AsyncSession,
    ) -> WorkflowExecuteResponse:
        """Execute a workflow"""

        # Generate trace ID
        trace_id = str(uuid.uuid4())
        set_trace_id(trace_id)

        logger.info(
            "workflow_execution_requested",
            workflow_id=workflow_id,
            user_id=user_id,
            trace_id=trace_id,
        )

        # Fetch workflow from database
        result = await db.execute(select(Workflow).where(Workflow.id == workflow_id))
        workflow = result.scalar_one_or_none()

        if not workflow:
            raise ValueError(f"Workflow not found: {workflow_id}")

        # Get workflow blocks and edges
        # TODO: Fetch from workflow_blocks and workflow_edges tables
        # For now, use empty structure for testing
        blocks = {}  # Will be populated from database
        edges = []  # Will be populated from database

        # Execute workflow
        execution_state = await self.executor.execute(
            workflow_id=workflow_id,
            user_id=user_id,
            blocks=blocks,
            edges=edges,
            input_data=execute_request.input,
            variables=execute_request.workflow_trigger_type,
            trace_id=trace_id,
        )

        # Save execution log
        execution_log = WorkflowExecutionLog(
            id=str(uuid.uuid4()),
            workflow_id=workflow_id,
            execution_id=execution_state.execution_id,
            level="info" if execution_state.status.value == "completed" else "error",
            trigger=execute_request.workflow_trigger_type,
            started_at=execution_state.started_at or datetime.utcnow(),
            ended_at=execution_state.ended_at,
            total_duration_ms=(
                int((execution_state.ended_at - execution_state.started_at).total_seconds() * 1000)
                if execution_state.started_at and execution_state.ended_at
                else None
            ),
            status=execution_state.status.value,
            input_data=execute_request.input,
            output_data=execution_state.output_data,
            error_message=execution_state.last_error,
            trace_id=trace_id,
            block_logs=[result.dict() for result in execution_state.block_results.values()],
            state_snapshot_id="temp-snapshot-id",  # TODO: Create proper snapshot
        )

        db.add(execution_log)
        await db.commit()

        # Build response
        response = WorkflowExecuteResponse(
            success=(execution_state.status.value == "completed"),
            execution_id=execution_state.execution_id,
            workflow_id=workflow_id,
            output=execution_state.output_data,
            logs=(
                [result.dict() for result in execution_state.block_results.values()]
                if not execute_request.stream
                else None
            ),
            metadata={
                "duration": execution_log.total_duration_ms,
                "blocks_executed": len(execution_state.executed_blocks),
            },
            trace_id=trace_id,
            started_at=execution_state.started_at or datetime.utcnow(),
            ended_at=execution_state.ended_at,
        )

        logger.info(
            "workflow_execution_response_created",
            execution_id=execution_state.execution_id,
            success=response.success,
        )

        return response
