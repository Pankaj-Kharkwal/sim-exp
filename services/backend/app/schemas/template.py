"""Template schemas"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class TemplateBase(BaseModel):
    """Base template schema"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    category: str = Field("other", pattern="^(marketing|sales|finance|support|ai|other)$")
    icon: str = Field("workflow", min_length=1, max_length=50)
    color: str = Field("#3972F6", pattern="^#[0-9A-Fa-f]{6}$")
    is_public: bool = Field(False)


class TemplateCreate(TemplateBase):
    """Schema for creating a template"""
    workflow_state: dict = Field(..., description="Complete workflow configuration")
    author_name: str = Field(..., min_length=1, max_length=255)
    author_avatar: Optional[str] = Field(None, max_length=500)


class TemplateUpdate(BaseModel):
    """Schema for updating a template"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    category: Optional[str] = Field(None, pattern="^(marketing|sales|finance|support|ai|other)$")
    icon: Optional[str] = Field(None, min_length=1, max_length=50)
    color: Optional[str] = Field(None, pattern="^#[0-9A-Fa-f]{6}$")
    is_public: Optional[bool] = None
    workflow_state: Optional[dict] = None


class TemplateStarCount(BaseModel):
    """Star count for a template"""
    count: int
    user_has_starred: bool


class TemplateResponse(TemplateBase):
    """Template response schema"""
    id: str
    workflow_state: dict
    views: int
    uses: int
    author_name: str
    author_avatar: Optional[str]
    user_id: str
    workspace_id: str
    created_at: datetime
    updated_at: datetime
    star_count: int = 0
    user_has_starred: bool = False

    class Config:
        from_attributes = True


class TemplateListItem(BaseModel):
    """Template list item (without full workflow_state)"""
    id: str
    name: str
    description: Optional[str]
    category: str
    icon: str
    color: str
    views: int
    uses: int
    is_public: bool
    author_name: str
    author_avatar: Optional[str]
    created_at: datetime
    updated_at: datetime
    star_count: int = 0
    user_has_starred: bool = False

    class Config:
        from_attributes = True


class TemplateListResponse(BaseModel):
    """Template list response with pagination"""
    templates: list[TemplateListItem]
    total: int
    page: int
    page_size: int
    total_pages: int


class UseTemplateRequest(BaseModel):
    """Request to use a template (create workflow from template)"""
    workflow_name: Optional[str] = Field(None, description="Custom name for new workflow")
    folder_id: Optional[str] = Field(None, description="Folder to place new workflow in")
