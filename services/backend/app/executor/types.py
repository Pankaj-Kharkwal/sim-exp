"""
Executor type definitions
"""
from typing import Any, Dict, Optional, Protocol
from pydantic import BaseModel
from enum import Enum


class BlockType(str, Enum):
    """Block type identifiers"""
    API = "api"
    FUNCTION = "function"
    CONDITION = "condition"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    SLACK = "slack"
    WEBHOOK = "webhook"
    RESPONSE = "response"
    VARIABLES = "variables"
    WAIT = "wait"
    ROUTER = "router"
    EVALUATOR = "evaluator"
    # ... add all 90+ block types


class ExecutionStatus(str, Enum):
    """Execution status"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ExecutionContext(BaseModel):
    """Execution context passed to block handlers"""
    execution_id: str
    workflow_id: str
    workspace_id: str
    user_id: Optional[str] = None
    variables: Dict[str, Any] = {}
    metadata: Dict[str, Any] = {}

    class Config:
        arbitrary_types_allowed = True


class BlockConfig(BaseModel):
    """Block configuration"""
    tool: str
    inputs: Dict[str, Any] = {}
    outputs: Dict[str, Any] = {}


class SerializedBlock(BaseModel):
    """Serialized block representation"""
    id: str
    type: str
    config: BlockConfig
    metadata: Dict[str, Any] = {}


class BlockResult(BaseModel):
    """Result from block execution"""
    success: bool
    output: Any = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = {}


class BlockHandler(Protocol):
    """Protocol for block handlers"""

    def can_handle(self, block: SerializedBlock) -> bool:
        """Check if this handler can process the block"""
        ...

    async def execute(
        self,
        ctx: ExecutionContext,
        block: SerializedBlock,
        inputs: Dict[str, Any],
    ) -> Any:
        """Execute the block"""
        ...
