"""Test database models"""

import pytest
from datetime import datetime, timedelta
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User, Session, Account, Verification
from app.db.models.organization import Organization, OrganizationMember, Workspace
from app.db.models.workflow import (
    Workflow,
    WorkflowBlock,
    WorkflowEdge,
    WorkflowFolder,
    WorkflowSubflow,
    WorkflowExecutionSnapshot,
    WorkflowExecutionLog,
)


@pytest.mark.asyncio
async def test_create_user(db_session: AsyncSession):
    """Test creating a user"""
    user = User(
        id=str(uuid.uuid4()),
        name="Test User",
        email="test@example.com",
        email_verified=False,
    )

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    assert user.id is not None
    assert user.name == "Test User"
    assert user.email == "test@example.com"
    assert user.created_at is not None
    assert user.updated_at is not None


@pytest.mark.asyncio
async def test_create_organization(db_session: AsyncSession):
    """Test creating an organization"""
    org = Organization(
        id=str(uuid.uuid4()),
        name="Test Org",
        slug="test-org",
    )

    db_session.add(org)
    await db_session.commit()
    await db_session.refresh(org)

    assert org.id is not None
    assert org.name == "Test Org"
    assert org.slug == "test-org"
    assert org.created_at is not None


@pytest.mark.asyncio
async def test_create_workflow(db_session: AsyncSession):
    """Test creating a workflow"""
    # Create user first
    user = User(
        id=str(uuid.uuid4()),
        name="Test User",
        email="workflow@example.com",
        email_verified=False,
    )
    db_session.add(user)
    await db_session.commit()

    # Create organization
    org = Organization(
        id=str(uuid.uuid4()),
        name="Test Org",
        slug="test-org-wf",
    )
    db_session.add(org)
    await db_session.commit()

    # Create workspace
    workspace = Workspace(
        id=str(uuid.uuid4()),
        name="Test Workspace",
        organization_id=org.id,
        owner_id=user.id,
    )
    db_session.add(workspace)
    await db_session.commit()

    # Create workflow
    workflow = Workflow(
        id=str(uuid.uuid4()),
        name="Test Workflow",
        description="A test workflow",
        user_id=user.id,
        workspace_id=workspace.id,
        last_synced=datetime.utcnow(),
    )

    db_session.add(workflow)
    await db_session.commit()
    await db_session.refresh(workflow)

    assert workflow.id is not None
    assert workflow.name == "Test Workflow"
    assert workflow.user_id == user.id
    assert workflow.workspace_id == workspace.id
    assert workflow.is_deployed is False
    assert workflow.run_count == 0


@pytest.mark.asyncio
async def test_workflow_with_blocks(db_session: AsyncSession):
    """Test creating a workflow with blocks and edges"""
    # Create user
    user = User(
        id=str(uuid.uuid4()),
        name="Test User",
        email="blocks@example.com",
        email_verified=False,
    )
    db_session.add(user)
    await db_session.commit()

    # Create workflow
    workflow = Workflow(
        id=str(uuid.uuid4()),
        name="Workflow with Blocks",
        user_id=user.id,
        last_synced=datetime.utcnow(),
    )
    db_session.add(workflow)
    await db_session.commit()

    # Create blocks
    block1 = WorkflowBlock(
        id=str(uuid.uuid4()),
        workflow_id=workflow.id,
        type="agent",
        name="Agent Block",
        position_x=100,
        position_y=100,
        data={"prompt": "Hello"},
    )
    block2 = WorkflowBlock(
        id=str(uuid.uuid4()),
        workflow_id=workflow.id,
        type="response",
        name="Response Block",
        position_x=300,
        position_y=100,
        data={},
    )

    db_session.add_all([block1, block2])
    await db_session.commit()

    # Create edge
    edge = WorkflowEdge(
        id=str(uuid.uuid4()),
        workflow_id=workflow.id,
        source_block_id=block1.id,
        target_block_id=block2.id,
    )
    db_session.add(edge)
    await db_session.commit()

    # Query workflow with blocks
    result = await db_session.execute(
        select(Workflow).where(Workflow.id == workflow.id)
    )
    loaded_workflow = result.scalar_one()

    assert len(loaded_workflow.blocks) == 2
    assert len(loaded_workflow.edges) == 1
    assert loaded_workflow.blocks[0].type == "agent"
    assert loaded_workflow.edges[0].source_block_id == block1.id


@pytest.mark.asyncio
async def test_workflow_execution_log(db_session: AsyncSession):
    """Test creating workflow execution log"""
    # Create user
    user = User(
        id=str(uuid.uuid4()),
        name="Test User",
        email="logs@example.com",
        email_verified=False,
    )
    db_session.add(user)
    await db_session.commit()

    # Create workflow
    workflow = Workflow(
        id=str(uuid.uuid4()),
        name="Test Workflow",
        user_id=user.id,
        last_synced=datetime.utcnow(),
    )
    db_session.add(workflow)
    await db_session.commit()

    # Create snapshot
    snapshot = WorkflowExecutionSnapshot(
        id=str(uuid.uuid4()),
        workflow_id=workflow.id,
        state_hash="abc123",
        state_data={"blocks": {}, "edges": []},
    )
    db_session.add(snapshot)
    await db_session.commit()

    # Create execution log
    execution_log = WorkflowExecutionLog(
        id=str(uuid.uuid4()),
        workflow_id=workflow.id,
        state_snapshot_id=snapshot.id,
        execution_id=str(uuid.uuid4()),
        level="info",
        trigger="api",
        started_at=datetime.utcnow(),
        status="running",
    )
    db_session.add(execution_log)
    await db_session.commit()
    await db_session.refresh(execution_log)

    assert execution_log.id is not None
    assert execution_log.workflow_id == workflow.id
    assert execution_log.status == "running"
    assert execution_log.trigger == "api"
