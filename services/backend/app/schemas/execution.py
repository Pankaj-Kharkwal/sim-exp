"""Execution schemas"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class BlockLogEntry(BaseModel):
    """Individual block execution log entry"""

    block_id: str
    block_type: str
    block_name: str
    started_at: datetime
    ended_at: Optional[datetime] = None
    duration_ms: Optional[int] = None
    status: str  # running, completed, failed, skipped
    input_data: Optional[dict[str, Any]] = None
    output_data: Optional[dict[str, Any]] = None
    error_message: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None  # tokens, cost, etc.


class ExecutionRead(BaseModel):
    """Execution read schema"""

    id: str
    execution_id: str
    workflow_id: str
    status: str  # running, completed, failed
    trigger: str  # api, webhook, schedule, manual, chat
    started_at: datetime
    ended_at: Optional[datetime] = None
    total_duration_ms: Optional[int] = None
    input_data: Optional[dict[str, Any]] = None
    output_data: Optional[dict[str, Any]] = None
    error_message: Optional[str] = None
    trace_id: Optional[str] = None

    model_config = {"from_attributes": True}


class ExecutionLogRead(BaseModel):
    """Detailed execution logs"""

    execution_id: str
    logs: list[BlockLogEntry]
    total_logs: int
    started_at: datetime
    ended_at: Optional[datetime] = None
    total_duration_ms: Optional[int] = None


class ExecutionTimelineEntry(BaseModel):
    """Timeline entry for visualization"""

    block_id: str
    block_type: str
    block_name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_ms: Optional[int] = None
    status: str
    parallel_group: Optional[int] = None  # For parallel execution visualization


class ExecutionTimelineRead(BaseModel):
    """Execution timeline for visualization"""

    execution_id: str
    timeline: list[ExecutionTimelineEntry]
    total_duration_ms: Optional[int] = None
    parallel_executions: int = Field(default=0, description="Number of parallel branches")
