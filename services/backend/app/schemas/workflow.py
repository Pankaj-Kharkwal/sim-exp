"""Workflow schemas - ALIGNED WITH NEXT.JS FRONTEND"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class Position(BaseModel):
    """Position structure matching frontend"""

    x: float
    y: float


class WorkflowBlockSchema(BaseModel):
    """Workflow block schema - matches frontend BlockState exactly"""

    id: str
    type: str
    name: str
    position: Position  # Frontend expects {x, y}, not separate fields
    enabled: bool = True
    horizontal_handles: Optional[bool] = Field(default=True, alias="horizontalHandles")
    is_wide: Optional[bool] = Field(default=False, alias="isWide")
    advanced_mode: Optional[bool] = Field(default=False, alias="advancedMode")
    trigger_mode: Optional[bool] = Field(default=False, alias="triggerMode")
    height: Optional[float] = Field(default=0)
    sub_blocks: dict[str, Any] = Field(default_factory=dict, alias="subBlocks")
    outputs: dict[str, Any] = Field(default_factory=dict)
    data: Optional[dict[str, Any]] = Field(default_factory=dict)

    model_config = {"populate_by_name": True}


class WorkflowEdgeSchema(BaseModel):
    """Workflow edge schema - matches frontend Edge exactly"""

    id: str
    source: str  # Frontend uses 'source', not 'source_block_id'
    target: str  # Frontend uses 'target', not 'target_block_id'
    source_handle: Optional[str] = Field(default=None, alias="sourceHandle")
    target_handle: Optional[str] = Field(default=None, alias="targetHandle")
    type: Optional[str] = None
    data: Optional[dict[str, Any]] = None

    model_config = {"populate_by_name": True}


class LoopSchema(BaseModel):
    """Loop structure for workflow"""

    id: str
    type: str = "loop"
    items: list[Any]
    max_iterations: Optional[int] = Field(default=100, alias="maxIterations")
    current_iteration: Optional[int] = Field(default=0, alias="currentIteration")

    model_config = {"populate_by_name": True}


class ParallelSchema(BaseModel):
    """Parallel execution structure for workflow"""

    id: str
    type: str = "parallel"
    branches: list[str]  # List of block IDs in parallel branches
    completed: Optional[list[str]] = Field(default_factory=list)

    model_config = {"populate_by_name": True}


class DeploymentStatus(BaseModel):
    """Deployment status for a version"""

    version: int
    deployed_at: datetime = Field(alias="deployedAt")
    is_active: bool = Field(alias="isActive")
    state_hash: str = Field(alias="stateHash")

    model_config = {"populate_by_name": True}


class WorkflowBase(BaseModel):
    """Base workflow schema"""

    name: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    color: str = Field(default="#3972F6", pattern="^#[0-9A-Fa-f]{6}$")
    variables: dict[str, Any] = Field(default_factory=dict)


class WorkflowCreate(WorkflowBase):
    """Workflow creation schema"""

    workspace_id: Optional[str] = Field(None, alias="workspaceId")
    folder_id: Optional[str] = Field(None, alias="folderId")
    is_published: Optional[bool] = Field(False, alias="isPublished")
    blocks: Optional[list[WorkflowBlockSchema]] = None
    edges: Optional[list[WorkflowEdgeSchema]] = None

    model_config = {"populate_by_name": True}


class WorkflowUpdate(BaseModel):
    """Workflow update schema"""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    is_published: Optional[bool] = Field(None, alias="isPublished")
    color: Optional[str] = Field(None, pattern="^#[0-9A-Fa-f]{6}$")
    blocks: Optional[list[WorkflowBlockSchema]] = None
    edges: Optional[list[WorkflowEdgeSchema]] = None
    loops: Optional[dict[str, LoopSchema]] = None
    parallels: Optional[dict[str, ParallelSchema]] = None
    variables: Optional[dict[str, Any]] = None


class WorkflowRead(WorkflowBase):
    """Workflow read schema - matches frontend WorkflowState"""

    id: str
    user_id: str = Field(alias="userId")
    organization_id: Optional[str] = Field(None, alias="organizationId")
    workspace_id: Optional[str] = Field(None, alias="workspaceId")
    folder_id: Optional[str] = Field(None, alias="folderId")
    is_deployed: bool = Field(alias="isDeployed")
    deployed_at: Optional[datetime] = Field(None, alias="deployedAt")
    needs_redeployment: Optional[bool] = Field(default=False, alias="needsRedeployment")
    run_count: int = Field(alias="runCount")
    last_run_at: Optional[datetime] = Field(None, alias="lastRunAt")
    last_saved: Optional[int] = Field(None, alias="lastSaved")  # Timestamp in ms
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")

    # Frontend expects these as dicts keyed by ID
    blocks: list[WorkflowBlockSchema] = Field(default_factory=list)
    edges: list[WorkflowEdgeSchema] = Field(default_factory=list)
    loops: dict[str, LoopSchema] = Field(default_factory=dict)
    parallels: dict[str, ParallelSchema] = Field(default_factory=dict)
    deployment_statuses: Optional[dict[str, DeploymentStatus]] = Field(
        None, alias="deploymentStatuses"
    )

    model_config = {"from_attributes": True, "populate_by_name": True}


class WorkflowStateResponse(BaseModel):
    """Workflow state response for /api/workflows/{id}/state endpoint"""

    blocks: list[WorkflowBlockSchema]
    edges: list[WorkflowEdgeSchema]
    loops: dict[str, LoopSchema]
    parallels: dict[str, ParallelSchema]
    variables: dict[str, Any]
    last_saved: Optional[int] = Field(None, alias="lastSaved")

    model_config = {"populate_by_name": True}


class WorkflowExecuteRequest(BaseModel):
    """Workflow execution request schema"""

    input: dict[str, Any] = Field(default_factory=dict)  # Frontend uses 'input', not 'input_data'
    stream: bool = False
    selected_outputs: Optional[list[str]] = Field(None, alias="selectedOutputs")
    workflow_trigger_type: str = Field(default="api", alias="workflowTriggerType")

    model_config = {"populate_by_name": True}


class WorkflowExecuteResponse(BaseModel):
    """Workflow execution response schema"""

    success: bool  # Frontend expects boolean, not status string
    execution_id: str = Field(alias="executionId")
    workflow_id: str = Field(alias="workflowId")
    output: Optional[dict[str, Any]] = None  # Frontend uses 'output', not 'output_data'
    logs: Optional[list[dict[str, Any]]] = None  # Inline logs for sync execution
    metadata: Optional[dict[str, Any]] = None  # duration, blocksExecuted, tokensUsed, cost
    trace_id: str = Field(alias="traceId")
    started_at: datetime = Field(alias="startedAt")
    ended_at: Optional[datetime] = Field(None, alias="endedAt")

    model_config = {"populate_by_name": True}


class WorkflowDeploymentCreate(BaseModel):
    """Create deployment request"""

    message: Optional[str] = None


class WorkflowDeploymentRead(BaseModel):
    """Deployment read schema"""

    id: str
    version: int
    workflow_id: str = Field(alias="workflowId")
    state_hash: str = Field(alias="stateHash")
    state_data: dict[str, Any] = Field(alias="stateData")
    is_active: bool = Field(alias="isActive")
    deployed_at: datetime = Field(alias="deployedAt")
    message: Optional[str] = None

    model_config = {"from_attributes": True, "populate_by_name": True}


class WorkflowResponse(BaseModel):
    """Generic workflow response wrapper - used by multiple endpoints"""

    workflow: WorkflowRead
    message: Optional[str] = None

    model_config = {"populate_by_name": True}


class WorkflowListResponse(BaseModel):
    """List of workflows response"""

    workflows: list[WorkflowRead]
    total: int
    page: int = 1
    page_size: int = Field(default=50, alias="pageSize")

    model_config = {"populate_by_name": True}


class WorkflowValidationResponse(BaseModel):
    """Workflow validation response"""

    valid: bool
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)

    model_config = {"populate_by_name": True}


class WorkflowStatsResponse(BaseModel):
    """Workflow stats response"""

    total_executions: int = Field(alias="totalExecutions")
    successful_executions: int = Field(alias="successfulExecutions")
    failed_executions: int = Field(alias="failedExecutions")
    average_duration_ms: float = Field(alias="averageDurationMs")
    total_tokens_used: Optional[int] = Field(None, alias="totalTokensUsed")
    total_cost: Optional[float] = Field(None, alias="totalCost")
    last_7_days: list[dict[str, Any]] = Field(default_factory=list, alias="last7Days")

    model_config = {"populate_by_name": True}
