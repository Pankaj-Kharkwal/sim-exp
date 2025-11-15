"""Template management endpoints"""

import uuid
from typing import Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select, func, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.logging import get_logger
from app.db.session import get_db
from app.db.models import WorkflowTemplate, TemplateStar, User, Workflow, WorkflowBlock, WorkflowEdge
from app.schemas.template import (
    TemplateCreate,
    TemplateUpdate,
    TemplateResponse,
    TemplateListItem,
    TemplateListResponse,
    UseTemplateRequest,
)
from app.schemas.workflow import WorkflowResponse

router = APIRouter()
logger = get_logger(__name__)


def get_current_user_id() -> str:
    """Get current user ID from auth - placeholder for now"""
    # TODO: Implement proper JWT auth
    return "demo-user-id"


def get_current_workspace_id() -> str:
    """Get current workspace ID from auth - placeholder for now"""
    # TODO: Implement proper workspace selection
    return "default"


@router.get("/", response_model=TemplateListResponse)
async def list_templates(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    sort_by: str = Query("created_at", pattern="^(created_at|views|uses|name)$"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$"),
    my_templates: bool = Query(False, description="Show only current user's templates"),
    db: AsyncSession = Depends(get_db),
):
    """
    List all templates

    - **skip**: Number of templates to skip (pagination)
    - **limit**: Maximum number of templates to return (max 100)
    - **category**: Filter by category (marketing, sales, finance, support, ai, other)
    - **search**: Search by name or description
    - **sort_by**: Sort field (created_at, views, uses, name)
    - **sort_order**: Sort order (asc, desc)
    - **my_templates**: Show only current user's templates
    """
    user_id = get_current_user_id()
    workspace_id = get_current_workspace_id()

    # Build query
    stmt = select(WorkflowTemplate)

    # Filter by user if my_templates is True
    if my_templates:
        stmt = stmt.where(WorkflowTemplate.user_id == user_id)
    else:
        # Show public templates or user's own templates
        stmt = stmt.where(
            or_(
                WorkflowTemplate.is_public == True,
                WorkflowTemplate.user_id == user_id
            )
        )

    # Filter by category
    if category:
        stmt = stmt.where(WorkflowTemplate.category == category)

    # Search
    if search:
        search_pattern = f"%{search}%"
        stmt = stmt.where(
            or_(
                WorkflowTemplate.name.ilike(search_pattern),
                WorkflowTemplate.description.ilike(search_pattern),
                WorkflowTemplate.author_name.ilike(search_pattern),
            )
        )

    # Count total
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total_result = await db.execute(count_stmt)
    total = total_result.scalar() or 0

    # Sort
    if sort_by == "created_at":
        order_col = WorkflowTemplate.created_at
    elif sort_by == "views":
        order_col = WorkflowTemplate.views
    elif sort_by == "uses":
        order_col = WorkflowTemplate.uses
    elif sort_by == "name":
        order_col = WorkflowTemplate.name
    else:
        order_col = WorkflowTemplate.created_at

    if sort_order == "desc":
        stmt = stmt.order_by(order_col.desc())
    else:
        stmt = stmt.order_by(order_col.asc())

    # Pagination
    stmt = stmt.offset(skip).limit(limit)

    # Execute
    result = await db.execute(stmt)
    templates = result.scalars().all()

    # Get star counts and user stars for each template
    template_list = []
    for template in templates:
        # Count stars
        star_count_stmt = select(func.count()).select_from(TemplateStar).where(
            TemplateStar.template_id == template.id
        )
        star_count_result = await db.execute(star_count_stmt)
        star_count = star_count_result.scalar() or 0

        # Check if user has starred
        user_star_stmt = select(TemplateStar).where(
            and_(
                TemplateStar.template_id == template.id,
                TemplateStar.user_id == user_id
            )
        )
        user_star_result = await db.execute(user_star_stmt)
        user_has_starred = user_star_result.scalar() is not None

        template_list.append(
            TemplateListItem(
                id=template.id,
                name=template.name,
                description=template.description,
                category=template.category,
                icon=template.icon,
                color=template.color,
                views=template.views,
                uses=template.uses,
                is_public=template.is_public,
                author_name=template.author_name,
                author_avatar=template.author_avatar,
                created_at=template.created_at,
                updated_at=template.updated_at,
                star_count=star_count,
                user_has_starred=user_has_starred,
            )
        )

    total_pages = (total + limit - 1) // limit if total > 0 else 0

    return TemplateListResponse(
        templates=template_list,
        total=total,
        page=skip // limit + 1,
        page_size=limit,
        total_pages=total_pages,
    )


@router.post("/", response_model=TemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_template(
    template_data: TemplateCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new template from a workflow
    """
    user_id = get_current_user_id()
    workspace_id = get_current_workspace_id()

    # Create template
    template_id = str(uuid.uuid4())
    template = WorkflowTemplate(
        id=template_id,
        name=template_data.name,
        description=template_data.description,
        category=template_data.category,
        icon=template_data.icon,
        color=template_data.color,
        workflow_state=template_data.workflow_state,
        is_public=template_data.is_public,
        author_name=template_data.author_name,
        author_avatar=template_data.author_avatar,
        user_id=user_id,
        workspace_id=workspace_id,
    )

    db.add(template)
    await db.commit()
    await db.refresh(template)

    logger.info("template_created", template_id=template_id, name=template_data.name)

    return TemplateResponse(
        id=template.id,
        name=template.name,
        description=template.description,
        category=template.category,
        icon=template.icon,
        color=template.color,
        workflow_state=template.workflow_state,
        views=template.views,
        uses=template.uses,
        is_public=template.is_public,
        author_name=template.author_name,
        author_avatar=template.author_avatar,
        user_id=template.user_id,
        workspace_id=template.workspace_id,
        created_at=template.created_at,
        updated_at=template.updated_at,
        star_count=0,
        user_has_starred=False,
    )


@router.get("/{template_id}", response_model=TemplateResponse)
async def get_template(
    template_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Get a template by ID and increment view count
    """
    user_id = get_current_user_id()

    # Get template
    stmt = select(WorkflowTemplate).where(WorkflowTemplate.id == template_id)
    result = await db.execute(stmt)
    template = result.scalar_one_or_none()

    if not template:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Template not found")

    # Check access (must be public or owned by user)
    if not template.is_public and template.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    # Increment view count
    template.views += 1
    await db.commit()

    # Get star count
    star_count_stmt = select(func.count()).select_from(TemplateStar).where(
        TemplateStar.template_id == template_id
    )
    star_count_result = await db.execute(star_count_stmt)
    star_count = star_count_result.scalar() or 0

    # Check if user has starred
    user_star_stmt = select(TemplateStar).where(
        and_(
            TemplateStar.template_id == template_id,
            TemplateStar.user_id == user_id
        )
    )
    user_star_result = await db.execute(user_star_stmt)
    user_has_starred = user_star_result.scalar() is not None

    return TemplateResponse(
        id=template.id,
        name=template.name,
        description=template.description,
        category=template.category,
        icon=template.icon,
        color=template.color,
        workflow_state=template.workflow_state,
        views=template.views,
        uses=template.uses,
        is_public=template.is_public,
        author_name=template.author_name,
        author_avatar=template.author_avatar,
        user_id=template.user_id,
        workspace_id=template.workspace_id,
        created_at=template.created_at,
        updated_at=template.updated_at,
        star_count=star_count,
        user_has_starred=user_has_starred,
    )


@router.put("/{template_id}", response_model=TemplateResponse)
async def update_template(
    template_id: str,
    template_data: TemplateUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    Update a template (only owner can update)
    """
    user_id = get_current_user_id()

    # Get template
    stmt = select(WorkflowTemplate).where(WorkflowTemplate.id == template_id)
    result = await db.execute(stmt)
    template = result.scalar_one_or_none()

    if not template:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Template not found")

    # Check ownership
    if template.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only owner can update template")

    # Update fields
    update_data = template_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(template, field, value)

    await db.commit()
    await db.refresh(template)

    # Get star count
    star_count_stmt = select(func.count()).select_from(TemplateStar).where(
        TemplateStar.template_id == template_id
    )
    star_count_result = await db.execute(star_count_stmt)
    star_count = star_count_result.scalar() or 0

    return TemplateResponse(
        id=template.id,
        name=template.name,
        description=template.description,
        category=template.category,
        icon=template.icon,
        color=template.color,
        workflow_state=template.workflow_state,
        views=template.views,
        uses=template.uses,
        is_public=template.is_public,
        author_name=template.author_name,
        author_avatar=template.author_avatar,
        user_id=template.user_id,
        workspace_id=template.workspace_id,
        created_at=template.created_at,
        updated_at=template.updated_at,
        star_count=star_count,
        user_has_starred=True,  # Owner always considered as starred
    )


@router.delete("/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_template(
    template_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Delete a template (only owner can delete)
    """
    user_id = get_current_user_id()

    # Get template
    stmt = select(WorkflowTemplate).where(WorkflowTemplate.id == template_id)
    result = await db.execute(stmt)
    template = result.scalar_one_or_none()

    if not template:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Template not found")

    # Check ownership
    if template.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only owner can delete template")

    await db.delete(template)
    await db.commit()

    logger.info("template_deleted", template_id=template_id)


@router.post("/{template_id}/star", status_code=status.HTTP_201_CREATED)
async def star_template(
    template_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Star a template
    """
    user_id = get_current_user_id()

    # Check if template exists
    stmt = select(WorkflowTemplate).where(WorkflowTemplate.id == template_id)
    result = await db.execute(stmt)
    template = result.scalar_one_or_none()

    if not template:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Template not found")

    # Check if already starred
    star_stmt = select(TemplateStar).where(
        and_(
            TemplateStar.template_id == template_id,
            TemplateStar.user_id == user_id
        )
    )
    star_result = await db.execute(star_stmt)
    existing_star = star_result.scalar_one_or_none()

    if existing_star:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Template already starred")

    # Create star
    star = TemplateStar(
        id=str(uuid.uuid4()),
        template_id=template_id,
        user_id=user_id,
    )

    db.add(star)
    await db.commit()

    logger.info("template_starred", template_id=template_id, user_id=user_id)

    return {"message": "Template starred successfully"}


@router.delete("/{template_id}/star", status_code=status.HTTP_204_NO_CONTENT)
async def unstar_template(
    template_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Unstar a template
    """
    user_id = get_current_user_id()

    # Find star
    stmt = select(TemplateStar).where(
        and_(
            TemplateStar.template_id == template_id,
            TemplateStar.user_id == user_id
        )
    )
    result = await db.execute(stmt)
    star = result.scalar_one_or_none()

    if not star:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Star not found")

    await db.delete(star)
    await db.commit()

    logger.info("template_unstarred", template_id=template_id, user_id=user_id)


@router.post("/{template_id}/use", response_model=WorkflowResponse, status_code=status.HTTP_201_CREATED)
async def use_template(
    template_id: str,
    request: UseTemplateRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new workflow from a template
    """
    user_id = get_current_user_id()
    workspace_id = get_current_workspace_id()

    # Get template
    stmt = select(WorkflowTemplate).where(WorkflowTemplate.id == template_id)
    result = await db.execute(stmt)
    template = result.scalar_one_or_none()

    if not template:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Template not found")

    # Check access
    if not template.is_public and template.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    # Increment use count
    template.uses += 1

    # Create new workflow from template
    workflow_id = str(uuid.uuid4())
    workflow_name = request.workflow_name or f"{template.name} (Copy)"

    # Create ID mapping for blocks
    old_to_new_id = {}
    workflow_state = template.workflow_state

    # Create workflow
    workflow = Workflow(
        id=workflow_id,
        name=workflow_name,
        description=template.description,
        color=template.color,
        user_id=user_id,
        workspace_id=workspace_id,
        folder_id=request.folder_id,
        last_synced=datetime.now(),
    )

    db.add(workflow)

    # Create blocks with new IDs
    if "blocks" in workflow_state:
        for block_data in workflow_state["blocks"]:
            old_block_id = block_data["id"]
            new_block_id = str(uuid.uuid4())
            old_to_new_id[old_block_id] = new_block_id

            block = WorkflowBlock(
                id=new_block_id,
                workflow_id=workflow_id,
                type=block_data.get("type", "agent"),
                name=block_data.get("name", "Block"),
                position_x=block_data.get("position", {}).get("x", 0),
                position_y=block_data.get("position", {}).get("y", 0),
                enabled=block_data.get("enabled", True),
                sub_blocks=block_data.get("subBlocks", {}),
                outputs=block_data.get("outputs", {}),
                data=block_data.get("data", {}),
            )
            db.add(block)

    # Create edges with new IDs
    if "edges" in workflow_state:
        for edge_data in workflow_state["edges"]:
            old_source = edge_data.get("source")
            old_target = edge_data.get("target")

            # Map old IDs to new IDs
            new_source = old_to_new_id.get(old_source)
            new_target = old_to_new_id.get(old_target)

            if new_source and new_target:
                edge = WorkflowEdge(
                    id=str(uuid.uuid4()),
                    workflow_id=workflow_id,
                    source_block_id=new_source,
                    target_block_id=new_target,
                    source_handle=edge_data.get("sourceHandle"),
                    target_handle=edge_data.get("targetHandle"),
                )
                db.add(edge)

    await db.commit()
    await db.refresh(workflow)

    logger.info("workflow_created_from_template", workflow_id=workflow_id, template_id=template_id)

    return WorkflowResponse(
        id=workflow.id,
        name=workflow.name,
        description=workflow.description,
        user_id=workflow.user_id,
        workspace_id=workflow.workspace_id,
        created_at=workflow.created_at,
        updated_at=workflow.updated_at,
        blocks=[],
        edges=[],
    )
