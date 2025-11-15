"""LangGraph-based workflow execution engine"""

import asyncio
import uuid
from datetime import datetime
from typing import Any, Optional

from langgraph.graph import StateGraph, END
from pydantic import BaseModel

from app.core.logging import get_logger
from app.executor.state import WorkflowState, ExecutionStatus, BlockResult

logger = get_logger(__name__)

# Import realtime notifier (optional - will be None if not available)
try:
    from app.realtime.execution_notifier import execution_notifier
except ImportError:
    execution_notifier = None
    logger.warning("realtime_notifier_not_available")

from app.executor.blocks.agent import execute_agent_block
from app.executor.blocks.api import execute_api_block
from app.executor.blocks.function import execute_function_block
from app.executor.blocks.condition import execute_condition_block
from app.executor.blocks.response import execute_response_block
from app.executor.blocks.http import execute_http_block
from app.executor.blocks.transformer import execute_transformer_block
from app.executor.blocks.database import execute_database_block
from app.executor.blocks.delay import execute_delay_block
from app.executor.blocks.webhook import execute_webhook_block
from app.executor.blocks.email import execute_email_block
from app.executor.blocks.variables import execute_variables_block
from app.executor.blocks.loop import execute_loop_block
from app.executor.blocks.parallel import execute_parallel_block
from app.executor.variable_resolver import resolve_variables


class WorkflowExecutor:
    """Workflow execution engine using LangGraph"""

    def __init__(self):
        self.block_executors = {
            # Core blocks
            "agent": execute_agent_block,
            "response": execute_response_block,

            # API & HTTP blocks
            "api": execute_api_block,
            "http": execute_http_block,
            "webhook": execute_webhook_block,

            # Control flow blocks
            "function": execute_function_block,
            "condition": execute_condition_block,
            "delay": execute_delay_block,
            "loop": execute_loop_block,
            "for_each": execute_loop_block,  # Alias
            "iterate": execute_loop_block,  # Alias
            "parallel": execute_parallel_block,
            "concurrent": execute_parallel_block,  # Alias
            "race": execute_parallel_block,  # Alias

            # Data transformation blocks
            "transformer": execute_transformer_block,
            "transform": execute_transformer_block,  # Alias

            # Database blocks
            "database": execute_database_block,
            "db": execute_database_block,  # Alias
            "postgresql": execute_database_block,
            "mongodb": execute_database_block,

            # Communication blocks
            "email": execute_email_block,

            # Variables blocks
            "variables": execute_variables_block,
            "var": execute_variables_block,  # Alias
            "set_variable": execute_variables_block,  # Alias
        }

    async def execute(
        self,
        workflow_id: str,
        user_id: str,
        blocks: dict[str, dict[str, Any]],
        edges: list[dict[str, Any]],
        input_data: dict[str, Any],
        variables: Optional[dict[str, Any]] = None,
        loops: Optional[dict[str, dict[str, Any]]] = None,
        parallels: Optional[dict[str, dict[str, Any]]] = None,
        trace_id: Optional[str] = None,
    ) -> WorkflowState:
        """Execute a workflow"""

        # Initialize execution state
        execution_id = str(uuid.uuid4())
        trace_id = trace_id or str(uuid.uuid4())

        state = WorkflowState(
            execution_id=execution_id,
            workflow_id=workflow_id,
            user_id=user_id,
            trace_id=trace_id,
            input_data=input_data,
            blocks=blocks,
            edges=edges,
            loops=loops or {},
            parallels=parallels or {},
            variables=variables or {},
            status=ExecutionStatus.RUNNING,
            started_at=datetime.utcnow(),
        )

        logger.info(
            "workflow_execution_started",
            execution_id=execution_id,
            workflow_id=workflow_id,
            trace_id=trace_id,
            blocks_count=len(blocks),
        )

        # Notify execution started via real-time
        if execution_notifier:
            try:
                await execution_notifier.notify_execution_started(
                    execution_id=execution_id,
                    workflow_id=workflow_id,
                    user_id=user_id,
                    input_data=input_data,
                )
            except Exception as e:
                logger.warning("failed_to_send_realtime_notification", error=str(e))

        try:
            # Build and execute the workflow graph
            state = await self._build_and_execute_graph(state)

            # Mark as completed
            state.status = ExecutionStatus.COMPLETED
            state.ended_at = datetime.utcnow()

            duration_ms = int((state.ended_at - state.started_at).total_seconds() * 1000) if state.started_at and state.ended_at else None

            logger.info(
                "workflow_execution_completed",
                execution_id=execution_id,
                blocks_executed=len(state.executed_blocks),
                duration_ms=duration_ms,
            )

            # Notify execution completed via real-time
            if execution_notifier:
                try:
                    await execution_notifier.notify_execution_completed(
                        execution_id=execution_id,
                        workflow_id=workflow_id,
                        user_id=user_id,
                        success=True,
                        output=state.output_data,
                        duration_ms=duration_ms,
                    )
                except Exception as e:
                    logger.warning("failed_to_send_realtime_notification", error=str(e))

        except Exception as e:
            state.status = ExecutionStatus.FAILED
            state.ended_at = datetime.utcnow()
            state.last_error = str(e)
            state.errors.append(str(e))

            logger.error(
                "workflow_execution_failed",
                execution_id=execution_id,
                error=str(e),
                exc_info=True,
            )

            # Notify execution failed via real-time
            if execution_notifier:
                try:
                    await execution_notifier.notify_execution_completed(
                        execution_id=execution_id,
                        workflow_id=workflow_id,
                        user_id=user_id,
                        success=False,
                        error=str(e),
                        duration_ms=int((state.ended_at - state.started_at).total_seconds() * 1000) if state.started_at and state.ended_at else None,
                    )
                except Exception as notif_error:
                    logger.warning("failed_to_send_realtime_notification", error=str(notif_error))

        return state

    async def _build_and_execute_graph(self, state: WorkflowState) -> WorkflowState:
        """Build LangGraph and execute workflow"""

        # For now, use simple sequential execution
        # TODO: Enhance with actual LangGraph state machine for complex flows

        # Find starter block (block with no incoming edges)
        starter_blocks = self._find_starter_blocks(state)

        if not starter_blocks:
            raise ValueError("No starter block found in workflow")

        # Execute blocks in topological order
        execution_order = self._topological_sort(state)

        logger.info(
            "execution_order_determined",
            execution_id=state.execution_id,
            order=execution_order,
        )

        for block_id in execution_order:
            block = state.blocks[block_id]

            # Skip if disabled
            if not block.get("enabled", True):
                logger.info("block_skipped_disabled", block_id=block_id)
                continue

            # Execute the block
            state = await self._execute_block(state, block_id, block)

            # Check for errors
            if state.status == ExecutionStatus.FAILED:
                break

        return state

    async def _execute_block(
        self, state: WorkflowState, block_id: str, block: dict[str, Any]
    ) -> WorkflowState:
        """Execute a single block"""

        block_type = block["type"]
        block_name = block["name"]

        logger.info(
            "block_execution_started",
            execution_id=state.execution_id,
            block_id=block_id,
            block_type=block_type,
            block_name=block_name,
        )

        # Notify block started via real-time
        if execution_notifier:
            try:
                await execution_notifier.notify_block_started(
                    execution_id=state.execution_id,
                    workflow_id=state.workflow_id,
                    block_id=block_id,
                    block_type=block_type,
                )
            except Exception as e:
                logger.warning("failed_to_send_realtime_notification", error=str(e))

        state.current_block_id = block_id
        started_at = datetime.utcnow()

        result = BlockResult(
            block_id=block_id,
            block_type=block_type,
            block_name=block_name,
            status=ExecutionStatus.RUNNING,
            started_at=started_at,
        )

        try:
            # Get the executor for this block type
            executor = self.block_executors.get(block_type)

            if not executor:
                raise ValueError(f"No executor found for block type: {block_type}")

            # Prepare input data by resolving variables
            input_data = self._prepare_block_input(state, block)

            result.input_data = input_data

            # Execute the block
            output = await executor(block, input_data, state)

            # Store output
            result.output_data = output
            result.status = ExecutionStatus.COMPLETED
            result.ended_at = datetime.utcnow()
            result.duration_ms = int((result.ended_at - started_at).total_seconds() * 1000)

            # Save to state
            state.set_block_output(block_id, output)
            state.executed_blocks.add(block_id)
            state.block_results[block_id] = result

            logger.info(
                "block_execution_completed",
                execution_id=state.execution_id,
                block_id=block_id,
                duration_ms=result.duration_ms,
            )

            # Notify block completed via real-time
            if execution_notifier:
                try:
                    await execution_notifier.notify_block_completed(
                        execution_id=state.execution_id,
                        workflow_id=state.workflow_id,
                        block_id=block_id,
                        block_type=block_type,
                        output=output,
                    )
                except Exception as e:
                    logger.warning("failed_to_send_realtime_notification", error=str(e))

        except Exception as e:
            result.status = ExecutionStatus.FAILED
            result.ended_at = datetime.utcnow()
            result.duration_ms = int((result.ended_at - started_at).total_seconds() * 1000)
            result.error_message = str(e)

            state.block_results[block_id] = result
            state.errors.append(f"Block {block_id} failed: {str(e)}")
            state.last_error = str(e)

            logger.error(
                "block_execution_failed",
                execution_id=state.execution_id,
                block_id=block_id,
                error=str(e),
                exc_info=True,
            )

            # Notify block failed via real-time
            if execution_notifier:
                try:
                    await execution_notifier.notify_block_failed(
                        execution_id=state.execution_id,
                        workflow_id=state.workflow_id,
                        block_id=block_id,
                        block_type=block_type,
                        error=str(e),
                    )
                except Exception as notif_error:
                    logger.warning("failed_to_send_realtime_notification", error=str(notif_error))

            # Stop execution on error
            state.status = ExecutionStatus.FAILED

        state.current_block_id = None
        return state

    def _prepare_block_input(
        self, state: WorkflowState, block: dict[str, Any]
    ) -> dict[str, Any]:
        """Prepare block input by resolving variables and references"""

        block_data = block.get("data", {})

        # Resolve all variables in block data using variable resolver
        input_data = resolve_variables(block_data, state)

        # Add workflow input for starter blocks
        if not state.executed_blocks:
            input_data["workflow_input"] = state.input_data

        return input_data

    def _find_starter_blocks(self, state: WorkflowState) -> list[str]:
        """Find blocks with no incoming edges (starter blocks)"""

        target_blocks = {edge["target"] for edge in state.edges}
        starter_blocks = [
            block_id for block_id in state.blocks.keys() if block_id not in target_blocks
        ]

        return starter_blocks

    def _topological_sort(self, state: WorkflowState) -> list[str]:
        """Topological sort of blocks based on edges"""

        # Build adjacency list
        graph: dict[str, list[str]] = {block_id: [] for block_id in state.blocks}
        in_degree: dict[str, int] = {block_id: 0 for block_id in state.blocks}

        for edge in state.edges:
            source = edge["source"]
            target = edge["target"]
            graph[source].append(target)
            in_degree[target] += 1

        # Kahn's algorithm
        queue = [block_id for block_id, degree in in_degree.items() if degree == 0]
        result = []

        while queue:
            block_id = queue.pop(0)
            result.append(block_id)

            for neighbor in graph[block_id]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        # Check for cycles
        if len(result) != len(state.blocks):
            raise ValueError("Workflow contains cycles")

        return result
