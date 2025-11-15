"""Workflow execution state management"""

from datetime import datetime
from typing import Any, Optional
from enum import Enum

from pydantic import BaseModel, Field


class ExecutionStatus(str, Enum):
    """Execution status enum"""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class BlockResult(BaseModel):
    """Result of a single block execution"""

    block_id: str
    block_type: str
    block_name: str
    status: ExecutionStatus
    started_at: datetime
    ended_at: Optional[datetime] = None
    duration_ms: Optional[int] = None
    input_data: Optional[dict[str, Any]] = None
    output_data: Optional[dict[str, Any]] = None
    error_message: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None  # tokens, cost, etc.


class WorkflowState(BaseModel):
    """Complete workflow execution state for LangGraph"""

    # Execution metadata
    execution_id: str
    workflow_id: str
    user_id: str
    status: ExecutionStatus = ExecutionStatus.PENDING
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None

    # Input/output
    input_data: dict[str, Any] = Field(default_factory=dict)
    output_data: dict[str, Any] = Field(default_factory=dict)

    # Workflow definition
    blocks: dict[str, dict[str, Any]] = Field(default_factory=dict)
    edges: list[dict[str, Any]] = Field(default_factory=list)
    loops: dict[str, dict[str, Any]] = Field(default_factory=dict)
    parallels: dict[str, dict[str, Any]] = Field(default_factory=dict)

    # Execution tracking
    current_block_id: Optional[str] = None
    executed_blocks: set[str] = Field(default_factory=set)
    block_results: dict[str, BlockResult] = Field(default_factory=dict)
    block_outputs: dict[str, dict[str, Any]] = Field(default_factory=dict)

    # Variables and context
    variables: dict[str, Any] = Field(default_factory=dict)
    context: dict[str, Any] = Field(default_factory=dict)

    # Error handling
    errors: list[str] = Field(default_factory=list)
    last_error: Optional[str] = None

    # Logging
    logs: list[dict[str, Any]] = Field(default_factory=list)
    trace_id: Optional[str] = None

    model_config = {"arbitrary_types_allowed": True}

    def add_log(self, level: str, message: str, **kwargs: Any) -> None:
        """Add a log entry"""
        self.logs.append(
            {
                "timestamp": datetime.utcnow().isoformat(),
                "level": level,
                "message": message,
                "block_id": self.current_block_id,
                **kwargs,
            }
        )

    def get_block_output(self, block_id: str) -> Optional[dict[str, Any]]:
        """Get output from a previously executed block"""
        return self.block_outputs.get(block_id)

    def set_block_output(self, block_id: str, output: dict[str, Any]) -> None:
        """Store block output for reference by other blocks"""
        self.block_outputs[block_id] = output

    def resolve_variable(self, var_ref: str) -> Any:
        """Resolve variable reference like {{blockId.output.field}}"""
        if not var_ref.startswith("{{") or not var_ref.endswith("}}"):
            return var_ref

        # Remove {{ and }}
        path = var_ref[2:-2].strip()

        # Check if it's a workflow variable
        if path.startswith("variables."):
            var_name = path.split(".", 1)[1]
            return self.variables.get(var_name)

        # Parse block output reference: blockId.output.field
        parts = path.split(".")
        if len(parts) < 2:
            return var_ref

        block_id = parts[0]
        block_output = self.get_block_output(block_id)

        if not block_output:
            return None

        # Navigate nested path
        result = block_output
        for part in parts[1:]:
            if isinstance(result, dict):
                result = result.get(part)
            else:
                return None

        return result

    def is_block_ready(self, block_id: str) -> bool:
        """Check if all dependencies for a block are satisfied"""
        # Find all edges pointing to this block
        for edge in self.edges:
            if edge["target"] == block_id:
                source_id = edge["source"]
                # Check if source block has been executed
                if source_id not in self.executed_blocks:
                    return False
        return True

    def get_next_blocks(self) -> list[str]:
        """Get list of blocks ready to execute"""
        ready_blocks = []

        for block_id, block in self.blocks.items():
            # Skip if already executed
            if block_id in self.executed_blocks:
                continue

            # Skip if disabled
            if not block.get("enabled", True):
                continue

            # Check if dependencies are satisfied
            if self.is_block_ready(block_id):
                ready_blocks.append(block_id)

        return ready_blocks
