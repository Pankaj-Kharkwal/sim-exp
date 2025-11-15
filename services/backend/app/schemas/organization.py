"""Organization Pydantic Schemas"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class OrganizationCreate(BaseModel):
    """Schema for creating an organization"""

    name: str = Field(..., min_length=1, max_length=255)
    display_name: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None


class OrganizationUpdate(BaseModel):
    """Schema for updating an organization"""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    display_name: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None


class OrganizationResponse(BaseModel):
    """Schema for organization response"""

    id: str
    name: str
    display_name: Optional[str]
    description: Optional[str]
    website: Optional[str]
    created_at: datetime
    updated_at: datetime
    member_count: Optional[int] = 0

    class Config:
        from_attributes = True


class OrganizationListResponse(BaseModel):
    """Schema for list of organizations"""

    organizations: List[OrganizationResponse]
    total: int


class WorkspaceCreate(BaseModel):
    """Schema for creating a workspace"""

    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    organization_id: str


class WorkspaceUpdate(BaseModel):
    """Schema for updating a workspace"""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None


class WorkspaceResponse(BaseModel):
    """Schema for workspace response"""

    id: str
    name: str
    description: Optional[str]
    organization_id: str
    created_at: datetime
    updated_at: datetime
    workflow_count: Optional[int] = 0
    member_count: Optional[int] = 0

    class Config:
        from_attributes = True


class WorkspaceListResponse(BaseModel):
    """Schema for list of workspaces"""

    workspaces: List[WorkspaceResponse]
    total: int


class OrganizationMemberInvite(BaseModel):
    """Schema for inviting a member"""

    email: str = Field(..., description="Email of the user to invite")
    role: str = Field(default="member", description="Role: owner, admin, member")


class OrganizationMemberResponse(BaseModel):
    """Schema for organization member"""

    user_id: str
    organization_id: str
    role: str
    email: Optional[str]
    name: Optional[str]
    joined_at: datetime

    class Config:
        from_attributes = True
