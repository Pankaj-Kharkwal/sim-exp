"""Organizations and Workspaces API Endpoints"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Body, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
import uuid
from datetime import datetime, timezone

from app.core.logging import get_logger
from app.core.auth import get_current_user
from app.db.session import get_db
from app.db.models.user import User
from app.db.models.organization import Organization, Workspace, OrganizationMember
from app.schemas.organization import (
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationResponse,
    OrganizationListResponse,
    WorkspaceCreate,
    WorkspaceUpdate,
    WorkspaceResponse,
    WorkspaceListResponse,
    OrganizationMemberInvite,
    OrganizationMemberResponse,
)

router = APIRouter()
logger = get_logger(__name__)


# Organization Endpoints
@router.get("/", response_model=OrganizationListResponse)
async def list_organizations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all organizations for the current user"""
    logger.info("list_organizations", skip=skip, limit=limit)

    user_id = current_user.id

    # Get organizations where user is a member
    query = (
        select(Organization)
        .join(OrganizationMember)
        .where(OrganizationMember.user_id == user_id)
        .options(selectinload(Organization.members))
    )

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # Apply pagination
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    orgs = result.scalars().all()

    return OrganizationListResponse(
        organizations=[
            OrganizationResponse(
                id=org.id,
                name=org.name,
                display_name=org.slug,
                description=org.description,
                website=None,
                created_at=org.created_at,
                updated_at=org.updated_at,
                member_count=len(org.members) if hasattr(org, 'members') else 0,
            )
            for org in orgs
        ],
        total=total,
    )


@router.post("/", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(
    org_data: OrganizationCreate = Body(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new organization"""
    logger.info("create_organization", name=org_data.name)

    user_id = current_user.id

    # Create organization
    now = datetime.utcnow()
    org = Organization(
        id=str(uuid.uuid4()),
        name=org_data.name,
        slug=org_data.name.lower().replace(" ", "-"),
        description=org_data.description,
        created_at=now,
        updated_at=now,
    )

    db.add(org)

    # Add creator as owner
    member = OrganizationMember(
        id=str(uuid.uuid4()),
        organization_id=org.id,
        user_id=user_id,
        role="owner",
        created_at=now,
        updated_at=now,
    )

    db.add(member)

    await db.commit()
    await db.refresh(org)

    logger.info("organization_created", org_id=org.id)

    return OrganizationResponse(
        id=org.id,
        name=org.name,
        display_name=org.slug,
        description=org.description,
        website=None,
        created_at=org.created_at,
        updated_at=org.updated_at,
        member_count=1,
    )


@router.get("/{org_id}", response_model=OrganizationResponse)
async def get_organization(
    org_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Get organization by ID"""
    logger.info("get_organization", org_id=org_id)

    query = select(Organization).where(Organization.id == org_id).options(
        selectinload(Organization.members)
    )

    result = await db.execute(query)
    org = result.scalar_one_or_none()

    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization not found: {org_id}",
        )

    return OrganizationResponse(
        id=org.id,
        name=org.name,
        display_name=org.slug,
        description=org.description,
        website=None,
        created_at=org.created_at,
        updated_at=org.updated_at,
        member_count=len(org.members) if hasattr(org, 'members') else 0,
    )


@router.put("/{org_id}", response_model=OrganizationResponse)
async def update_organization(
    org_id: str,
    org_data: OrganizationUpdate = Body(...),
    db: AsyncSession = Depends(get_db),
):
    """Update organization"""
    logger.info("update_organization", org_id=org_id)

    query = select(Organization).where(Organization.id == org_id)
    result = await db.execute(query)
    org = result.scalar_one_or_none()

    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization not found: {org_id}",
        )

    # Update fields
    update_data = org_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field == "name":
            org.name = value
            org.slug = value.lower().replace(" ", "-")
        elif field == "description":
            org.description = value

    await db.commit()
    await db.refresh(org)

    logger.info("organization_updated", org_id=org_id)

    return OrganizationResponse(
        id=org.id,
        name=org.name,
        display_name=org.slug,
        description=org.description,
        website=None,
        created_at=org.created_at,
        updated_at=org.updated_at,
        member_count=0,
    )


@router.delete("/{org_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(
    org_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Delete organization"""
    logger.info("delete_organization", org_id=org_id)

    query = select(Organization).where(Organization.id == org_id)
    result = await db.execute(query)
    org = result.scalar_one_or_none()

    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization not found: {org_id}",
        )

    await db.delete(org)
    await db.commit()

    logger.info("organization_deleted", org_id=org_id)
    return None


# Workspace Endpoints
@router.get("/{org_id}/workspaces", response_model=WorkspaceListResponse)
async def list_workspaces(
    org_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List all workspaces in an organization"""
    logger.info("list_workspaces", org_id=org_id, skip=skip, limit=limit)

    query = select(Workspace).where(Workspace.organization_id == org_id)

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # Apply pagination
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    workspaces = result.scalars().all()

    return WorkspaceListResponse(
        workspaces=[
            WorkspaceResponse(
                id=ws.id,
                name=ws.name,
                description=ws.description,
                organization_id=ws.organization_id,
                created_at=ws.created_at,
                updated_at=ws.updated_at,
                workflow_count=0,  # TODO: Calculate
                member_count=0,  # TODO: Calculate
            )
            for ws in workspaces
        ],
        total=total,
    )


@router.post("/{org_id}/workspaces", response_model=WorkspaceResponse, status_code=status.HTTP_201_CREATED)
async def create_workspace(
    org_id: str,
    ws_data: WorkspaceCreate = Body(...),
    db: AsyncSession = Depends(get_db),
):
    """Create a new workspace in an organization"""
    logger.info("create_workspace", org_id=org_id, name=ws_data.name)

    user_id = get_current_user_id()

    # Create workspace
    ws = Workspace(
        id=str(uuid.uuid4()),
        name=ws_data.name,
        description=ws_data.description,
        organization_id=org_id,
        owner_id=user_id,
        is_default=False,
    )

    db.add(ws)
    await db.commit()
    await db.refresh(ws)

    logger.info("workspace_created", workspace_id=ws.id)

    return WorkspaceResponse(
        id=ws.id,
        name=ws.name,
        description=ws.description,
        organization_id=ws.organization_id,
        created_at=ws.created_at,
        updated_at=ws.updated_at,
        workflow_count=0,
        member_count=0,
    )


@router.get("/{org_id}/workspaces/{workspace_id}", response_model=WorkspaceResponse)
async def get_workspace(
    org_id: str,
    workspace_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Get workspace by ID"""
    logger.info("get_workspace", org_id=org_id, workspace_id=workspace_id)

    query = select(Workspace).where(
        Workspace.id == workspace_id,
        Workspace.organization_id == org_id,
    )

    result = await db.execute(query)
    ws = result.scalar_one_or_none()

    if not ws:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workspace not found: {workspace_id}",
        )

    return WorkspaceResponse(
        id=ws.id,
        name=ws.name,
        description=ws.description,
        organization_id=ws.organization_id,
        created_at=ws.created_at,
        updated_at=ws.updated_at,
        workflow_count=0,  # TODO: Calculate
        member_count=0,  # TODO: Calculate
    )


@router.put("/{org_id}/workspaces/{workspace_id}", response_model=WorkspaceResponse)
async def update_workspace(
    org_id: str,
    workspace_id: str,
    ws_data: WorkspaceUpdate = Body(...),
    db: AsyncSession = Depends(get_db),
):
    """Update workspace"""
    logger.info("update_workspace", org_id=org_id, workspace_id=workspace_id)

    query = select(Workspace).where(
        Workspace.id == workspace_id,
        Workspace.organization_id == org_id,
    )

    result = await db.execute(query)
    ws = result.scalar_one_or_none()

    if not ws:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workspace not found: {workspace_id}",
        )

    # Update fields
    update_data = ws_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(ws, field, value)

    await db.commit()
    await db.refresh(ws)

    logger.info("workspace_updated", workspace_id=workspace_id)

    return WorkspaceResponse(
        id=ws.id,
        name=ws.name,
        description=ws.description,
        organization_id=ws.organization_id,
        created_at=ws.created_at,
        updated_at=ws.updated_at,
        workflow_count=0,
        member_count=0,
    )


@router.delete("/{org_id}/workspaces/{workspace_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workspace(
    org_id: str,
    workspace_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Delete workspace"""
    logger.info("delete_workspace", org_id=org_id, workspace_id=workspace_id)

    query = select(Workspace).where(
        Workspace.id == workspace_id,
        Workspace.organization_id == org_id,
    )

    result = await db.execute(query)
    ws = result.scalar_one_or_none()

    if not ws:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workspace not found: {workspace_id}",
        )

    await db.delete(ws)
    await db.commit()

    logger.info("workspace_deleted", workspace_id=workspace_id)
    return None


# Member Endpoints
@router.get("/{org_id}/members", response_model=List[OrganizationMemberResponse])
async def list_organization_members(
    org_id: str,
    db: AsyncSession = Depends(get_db),
):
    """List all members of an organization"""
    logger.info("list_organization_members", org_id=org_id)

    query = (
        select(OrganizationMember)
        .where(OrganizationMember.organization_id == org_id)
        .options(selectinload(OrganizationMember.user))
    )

    result = await db.execute(query)
    members = result.scalars().all()

    return [
        OrganizationMemberResponse(
            user_id=member.user_id,
            organization_id=member.organization_id,
            role=member.role,
            email=None,  # TODO: Get from user
            name=None,  # TODO: Get from user
            joined_at=member.created_at,
        )
        for member in members
    ]


@router.post("/{org_id}/members/invite", response_model=OrganizationMemberResponse)
async def invite_organization_member(
    org_id: str,
    invite_data: OrganizationMemberInvite = Body(...),
    db: AsyncSession = Depends(get_db),
):
    """Invite a new member to the organization"""
    logger.info("invite_organization_member", org_id=org_id, email=invite_data.email)

    # TODO: Send invitation email
    # TODO: Create pending invitation record

    # For now, just return a placeholder
    return OrganizationMemberResponse(
        user_id="pending",
        organization_id=org_id,
        role=invite_data.role,
        email=invite_data.email,
        name=None,
        joined_at=None,
    )
