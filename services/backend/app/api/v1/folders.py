"""Folders API Endpoints"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Body, Query
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
import uuid

from app.core.logging import get_logger
from app.db.session import get_db
from app.db.models.folder import Folder
from app.schemas.folder import (
    FolderCreate,
    FolderUpdate,
    FolderResponse,
    FolderListResponse,
    FolderTreeNode,
    FolderMoveRequest,
)

router = APIRouter()
logger = get_logger(__name__)


def get_current_user_id() -> str:
    """Get current user ID - placeholder"""
    return "demo-user-id"


def get_current_organization_id() -> str:
    """Get current organization ID - placeholder"""
    return "demo-org-id"


def build_folder_path(parent_path: Optional[str], folder_name: str) -> str:
    """Build full path for a folder"""
    if parent_path:
        return f"{parent_path}/{folder_name}"
    return f"/{folder_name}"


async def get_folder_level(parent_id: Optional[str], db: AsyncSession) -> int:
    """Get the level of a folder based on its parent"""
    if not parent_id:
        return 0

    query = select(Folder.level).where(Folder.id == parent_id)
    result = await db.execute(query)
    parent_level = result.scalar_one_or_none()

    return (parent_level + 1) if parent_level is not None else 0


@router.get("/", response_model=FolderListResponse)
async def list_folders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    parent_id: Optional[str] = Query(None, description="Filter by parent folder"),
    db: AsyncSession = Depends(get_db),
):
    """List all folders"""
    logger.info("list_folders", skip=skip, limit=limit, parent_id=parent_id)

    user_id = get_current_user_id()
    org_id = get_current_organization_id()

    query = select(Folder).where(
        Folder.user_id == user_id,
        Folder.organization_id == org_id,
    )

    # Filter by parent
    if parent_id:
        query = query.where(Folder.parent_id == parent_id)
    else:
        # Root folders only
        query = query.where(Folder.parent_id.is_(None))

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # Apply pagination and ordering
    query = query.order_by(Folder.name).offset(skip).limit(limit)
    result = await db.execute(query)
    folders = result.scalars().all()

    return FolderListResponse(
        folders=[
            FolderResponse(
                id=folder.id,
                name=folder.name,
                description=folder.description,
                parent_id=folder.parent_id,
                path=folder.path,
                level=folder.level,
                user_id=folder.user_id,
                organization_id=folder.organization_id,
                color=folder.color,
                icon=folder.icon,
                workflow_count=folder.workflow_count,
                subfolder_count=folder.subfolder_count,
                created_at=folder.created_at,
                updated_at=folder.updated_at,
            )
            for folder in folders
        ],
        total=total,
        skip=skip,
        limit=limit,
    )


@router.post("/", response_model=FolderResponse, status_code=status.HTTP_201_CREATED)
async def create_folder(
    folder_data: FolderCreate = Body(...),
    db: AsyncSession = Depends(get_db),
):
    """Create a new folder"""
    logger.info("create_folder", name=folder_data.name, parent_id=folder_data.parent_id)

    user_id = get_current_user_id()
    org_id = get_current_organization_id()

    # Get parent folder if specified
    parent_path = "/"
    if folder_data.parent_id:
        parent_query = select(Folder).where(Folder.id == folder_data.parent_id)
        parent_result = await db.execute(parent_query)
        parent_folder = parent_result.scalar_one_or_none()

        if not parent_folder:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Parent folder not found: {folder_data.parent_id}",
            )

        parent_path = parent_folder.path

    # Calculate level
    level = await get_folder_level(folder_data.parent_id, db)

    # Build path
    path = build_folder_path(parent_path if folder_data.parent_id else None, folder_data.name)

    # Create folder
    folder = Folder(
        id=str(uuid.uuid4()),
        name=folder_data.name,
        description=folder_data.description,
        parent_id=folder_data.parent_id,
        path=path,
        level=level,
        user_id=user_id,
        organization_id=org_id,
        color=folder_data.color,
        icon=folder_data.icon,
        workflow_count=0,
        subfolder_count=0,
    )

    db.add(folder)

    # Update parent subfolder count
    if folder_data.parent_id:
        parent_update = (
            select(Folder)
            .where(Folder.id == folder_data.parent_id)
        )
        parent_result = await db.execute(parent_update)
        parent = parent_result.scalar_one_or_none()
        if parent:
            parent.subfolder_count += 1

    await db.commit()
    await db.refresh(folder)

    logger.info("folder_created", folder_id=folder.id)

    return FolderResponse(
        id=folder.id,
        name=folder.name,
        description=folder.description,
        parent_id=folder.parent_id,
        path=folder.path,
        level=folder.level,
        user_id=folder.user_id,
        organization_id=folder.organization_id,
        color=folder.color,
        icon=folder.icon,
        workflow_count=folder.workflow_count,
        subfolder_count=folder.subfolder_count,
        created_at=folder.created_at,
        updated_at=folder.updated_at,
    )


@router.get("/{folder_id}", response_model=FolderResponse)
async def get_folder(
    folder_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Get folder by ID"""
    logger.info("get_folder", folder_id=folder_id)

    query = select(Folder).where(Folder.id == folder_id)
    result = await db.execute(query)
    folder = result.scalar_one_or_none()

    if not folder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Folder not found: {folder_id}",
        )

    return FolderResponse(
        id=folder.id,
        name=folder.name,
        description=folder.description,
        parent_id=folder.parent_id,
        path=folder.path,
        level=folder.level,
        user_id=folder.user_id,
        organization_id=folder.organization_id,
        color=folder.color,
        icon=folder.icon,
        workflow_count=folder.workflow_count,
        subfolder_count=folder.subfolder_count,
        created_at=folder.created_at,
        updated_at=folder.updated_at,
    )


@router.put("/{folder_id}", response_model=FolderResponse)
async def update_folder(
    folder_id: str,
    folder_data: FolderUpdate = Body(...),
    db: AsyncSession = Depends(get_db),
):
    """Update folder"""
    logger.info("update_folder", folder_id=folder_id)

    query = select(Folder).where(Folder.id == folder_id)
    result = await db.execute(query)
    folder = result.scalar_one_or_none()

    if not folder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Folder not found: {folder_id}",
        )

    # Update fields
    update_data = folder_data.model_dump(exclude_unset=True)

    # Handle name change (update path)
    if "name" in update_data and update_data["name"] != folder.name:
        old_path = folder.path
        new_path = "/".join(old_path.split("/")[:-1]) + "/" + update_data["name"]
        folder.path = new_path

        # Update all child paths recursively
        # TODO: Implement recursive path update for children

    for field, value in update_data.items():
        if field not in ["parent_id"]:  # Don't allow parent_id change via update
            setattr(folder, field, value)

    await db.commit()
    await db.refresh(folder)

    logger.info("folder_updated", folder_id=folder_id)

    return FolderResponse(
        id=folder.id,
        name=folder.name,
        description=folder.description,
        parent_id=folder.parent_id,
        path=folder.path,
        level=folder.level,
        user_id=folder.user_id,
        organization_id=folder.organization_id,
        color=folder.color,
        icon=folder.icon,
        workflow_count=folder.workflow_count,
        subfolder_count=folder.subfolder_count,
        created_at=folder.created_at,
        updated_at=folder.updated_at,
    )


@router.delete("/{folder_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_folder(
    folder_id: str,
    recursive: bool = Query(False, description="Delete subfolders and workflows"),
    db: AsyncSession = Depends(get_db),
):
    """Delete folder"""
    logger.info("delete_folder", folder_id=folder_id, recursive=recursive)

    query = select(Folder).where(Folder.id == folder_id).options(
        selectinload(Folder.subfolders)
    )
    result = await db.execute(query)
    folder = result.scalar_one_or_none()

    if not folder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Folder not found: {folder_id}",
        )

    # Check if folder has children
    if not recursive and folder.subfolder_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Folder has subfolders. Use recursive=true to delete them.",
        )

    if not recursive and folder.workflow_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Folder has workflows. Use recursive=true to delete them.",
        )

    # Update parent subfolder count
    if folder.parent_id:
        parent_query = select(Folder).where(Folder.id == folder.parent_id)
        parent_result = await db.execute(parent_query)
        parent = parent_result.scalar_one_or_none()
        if parent:
            parent.subfolder_count -= 1

    await db.delete(folder)
    await db.commit()

    logger.info("folder_deleted", folder_id=folder_id)
    return None


@router.post("/{folder_id}/move", response_model=FolderResponse)
async def move_folder(
    folder_id: str,
    move_data: FolderMoveRequest = Body(...),
    db: AsyncSession = Depends(get_db),
):
    """Move folder to a different parent"""
    logger.info("move_folder", folder_id=folder_id, target_parent_id=move_data.target_parent_id)

    query = select(Folder).where(Folder.id == folder_id)
    result = await db.execute(query)
    folder = result.scalar_one_or_none()

    if not folder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Folder not found: {folder_id}",
        )

    # Prevent moving folder into itself or its descendants
    if move_data.target_parent_id == folder_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot move folder into itself",
        )

    # Update old parent subfolder count
    if folder.parent_id:
        old_parent_query = select(Folder).where(Folder.id == folder.parent_id)
        old_parent_result = await db.execute(old_parent_query)
        old_parent = old_parent_result.scalar_one_or_none()
        if old_parent:
            old_parent.subfolder_count -= 1

    # Get new parent
    new_parent_path = "/"
    if move_data.target_parent_id:
        new_parent_query = select(Folder).where(Folder.id == move_data.target_parent_id)
        new_parent_result = await db.execute(new_parent_query)
        new_parent = new_parent_result.scalar_one_or_none()

        if not new_parent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Target parent folder not found: {move_data.target_parent_id}",
            )

        new_parent_path = new_parent.path
        new_parent.subfolder_count += 1

    # Update folder
    folder.parent_id = move_data.target_parent_id
    folder.level = await get_folder_level(move_data.target_parent_id, db)
    folder.path = build_folder_path(
        new_parent_path if move_data.target_parent_id else None,
        folder.name
    )

    # TODO: Update all child paths recursively

    await db.commit()
    await db.refresh(folder)

    logger.info("folder_moved", folder_id=folder_id, new_parent_id=move_data.target_parent_id)

    return FolderResponse(
        id=folder.id,
        name=folder.name,
        description=folder.description,
        parent_id=folder.parent_id,
        path=folder.path,
        level=folder.level,
        user_id=folder.user_id,
        organization_id=folder.organization_id,
        color=folder.color,
        icon=folder.icon,
        workflow_count=folder.workflow_count,
        subfolder_count=folder.subfolder_count,
        created_at=folder.created_at,
        updated_at=folder.updated_at,
    )


@router.get("/tree", response_model=List[FolderTreeNode])
async def get_folder_tree(
    db: AsyncSession = Depends(get_db),
):
    """Get folder tree structure"""
    logger.info("get_folder_tree")

    user_id = get_current_user_id()
    org_id = get_current_organization_id()

    query = select(Folder).where(
        Folder.user_id == user_id,
        Folder.organization_id == org_id,
    ).order_by(Folder.level, Folder.name)

    result = await db.execute(query)
    folders = result.scalars().all()

    # Build tree structure
    folder_map = {}
    root_folders = []

    for folder in folders:
        node = FolderTreeNode(
            id=folder.id,
            name=folder.name,
            description=folder.description,
            color=folder.color,
            icon=folder.icon,
            workflow_count=folder.workflow_count,
            subfolder_count=folder.subfolder_count,
            parent_id=folder.parent_id,
            children=[],
        )
        folder_map[folder.id] = node

    # Connect parents and children
    for folder in folders:
        node = folder_map[folder.id]
        if folder.parent_id and folder.parent_id in folder_map:
            folder_map[folder.parent_id].children.append(node)
        else:
            root_folders.append(node)

    logger.info("folder_tree_retrieved", root_count=len(root_folders))
    return root_folders
