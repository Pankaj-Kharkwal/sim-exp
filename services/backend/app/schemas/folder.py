"""Folder Pydantic Schemas"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class FolderCreate(BaseModel):
    """Schema for creating a folder"""

    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    parent_id: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[str] = None


class FolderUpdate(BaseModel):
    """Schema for updating a folder"""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    parent_id: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[str] = None


class FolderResponse(BaseModel):
    """Schema for folder response"""

    id: str
    name: str
    description: Optional[str]
    parent_id: Optional[str]
    path: str
    level: int
    user_id: str
    organization_id: str
    color: Optional[str]
    icon: Optional[str]
    workflow_count: int
    subfolder_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class FolderListResponse(BaseModel):
    """Schema for list of folders"""

    folders: List[FolderResponse]
    total: int
    skip: int
    limit: int


class FolderTreeNode(BaseModel):
    """Schema for folder tree node"""

    id: str
    name: str
    description: Optional[str]
    color: Optional[str]
    icon: Optional[str]
    workflow_count: int
    subfolder_count: int
    parent_id: Optional[str]
    children: List["FolderTreeNode"] = []

    class Config:
        from_attributes = True


class FolderMoveRequest(BaseModel):
    """Schema for moving a folder"""

    target_parent_id: Optional[str] = Field(
        None,
        description="ID of the new parent folder, or None for root",
    )
