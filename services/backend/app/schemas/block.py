"""Block schemas"""

from typing import Any, Optional

from pydantic import BaseModel, Field


class BlockConfigSchema(BaseModel):
    """Block configuration schema"""

    type: str
    required: bool = False
    default: Optional[Any] = None
    description: Optional[str] = None


class BlockRead(BaseModel):
    """Block type read schema"""

    type: str
    name: str
    category: str  # processing, logic, control_flow, output
    description: str
    config_schema: dict[str, BlockConfigSchema]
    icon: Optional[str] = None
    color: Optional[str] = None


class BlockGenerateRequest(BaseModel):
    """AI block generation request"""

    description: str = Field(
        min_length=10,
        max_length=500,
        description="Description of what the block should do",
        examples=["Send a Slack message with file attachment", "Query MongoDB database"],
    )
    research: bool = Field(
        default=True, description="Whether to research the API/service first"
    )
    api_provider: Optional[str] = Field(
        None, description="Specific API provider if known (e.g., 'slack', 'github')"
    )


class BlockGenerateResponse(BaseModel):
    """AI block generation response"""

    block: BlockRead
    implementation_code: Optional[str] = Field(
        None, description="Generated implementation code"
    )
    ui_schema: Optional[dict[str, Any]] = Field(None, description="Generated UI configuration")
    research_notes: Optional[str] = Field(
        None, description="Research findings about the API"
    )
    confidence: float = Field(
        ge=0.0, le=1.0, description="Confidence score of the generation"
    )
