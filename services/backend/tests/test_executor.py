"""Test workflow executor"""

import pytest
from datetime import datetime

from app.executor.engine import WorkflowExecutor
from app.executor.state import ExecutionStatus


@pytest.mark.asyncio
async def test_executor_initialization():
    """Test executor initializes correctly"""
    executor = WorkflowExecutor()
    assert executor is not None
    assert "agent" in executor.block_executors
    assert "api" in executor.block_executors
    assert "function" in executor.block_executors
    assert "condition" in executor.block_executors
    assert "response" in executor.block_executors


@pytest.mark.asyncio
async def test_simple_workflow_execution():
    """Test executing a simple workflow"""
    executor = WorkflowExecutor()

    # Simple workflow: response block only
    blocks = {
        "block-1": {
            "id": "block-1",
            "type": "response",
            "name": "Response",
            "enabled": True,
            "data": {
                "message": "Hello World",
            },
        }
    }

    edges = []

    result = await executor.execute(
        workflow_id="test-workflow",
        user_id="test-user",
        blocks=blocks,
        edges=edges,
        input_data={"test": "input"},
    )

    assert result is not None
    assert result.execution_id is not None
    assert result.workflow_id == "test-workflow"
    assert result.status == ExecutionStatus.COMPLETED
    assert len(result.executed_blocks) == 1
    assert "block-1" in result.executed_blocks
    assert result.started_at is not None
    assert result.ended_at is not None


@pytest.mark.asyncio
async def test_workflow_with_two_blocks():
    """Test executing workflow with two connected blocks"""
    executor = WorkflowExecutor()

    blocks = {
        "block-1": {
            "id": "block-1",
            "type": "response",
            "name": "First",
            "enabled": True,
            "data": {"message": "First block"},
        },
        "block-2": {
            "id": "block-2",
            "type": "response",
            "name": "Second",
            "enabled": True,
            "data": {"message": "Second block"},
        },
    }

    edges = [
        {
            "id": "edge-1",
            "source": "block-1",
            "target": "block-2",
        }
    ]

    result = await executor.execute(
        workflow_id="test-workflow",
        user_id="test-user",
        blocks=blocks,
        edges=edges,
        input_data={},
    )

    assert result.status == ExecutionStatus.COMPLETED
    assert len(result.executed_blocks) == 2
    assert "block-1" in result.executed_blocks
    assert "block-2" in result.executed_blocks
    assert len(result.block_results) == 2


@pytest.mark.asyncio
async def test_disabled_block_skipped():
    """Test that disabled blocks are skipped"""
    executor = WorkflowExecutor()

    blocks = {
        "block-1": {
            "id": "block-1",
            "type": "response",
            "name": "Enabled",
            "enabled": True,
            "data": {},
        },
        "block-2": {
            "id": "block-2",
            "type": "response",
            "name": "Disabled",
            "enabled": False,  # This should be skipped
            "data": {},
        },
    }

    edges = [{"id": "edge-1", "source": "block-1", "target": "block-2"}]

    result = await executor.execute(
        workflow_id="test-workflow",
        user_id="test-user",
        blocks=blocks,
        edges=edges,
        input_data={},
    )

    assert result.status == ExecutionStatus.COMPLETED
    assert len(result.executed_blocks) == 1  # Only enabled block
    assert "block-1" in result.executed_blocks
    assert "block-2" not in result.executed_blocks


@pytest.mark.asyncio
async def test_topological_sort():
    """Test topological sorting of blocks"""
    executor = WorkflowExecutor()

    blocks = {
        "a": {"id": "a", "type": "response", "name": "A", "enabled": True, "data": {}},
        "b": {"id": "b", "type": "response", "name": "B", "enabled": True, "data": {}},
        "c": {"id": "c", "type": "response", "name": "C", "enabled": True, "data": {}},
    }

    edges = [
        {"id": "e1", "source": "a", "target": "b"},
        {"id": "e2", "source": "b", "target": "c"},
    ]

    # Create minimal state for testing
    class MockState:
        def __init__(self):
            self.blocks = blocks
            self.edges = edges

    state = MockState()
    order = executor._topological_sort(state)

    # A should come before B, B should come before C
    assert order.index("a") < order.index("b")
    assert order.index("b") < order.index("c")


@pytest.mark.asyncio
async def test_invalid_block_type():
    """Test execution with invalid block type"""
    executor = WorkflowExecutor()

    blocks = {
        "block-1": {
            "id": "block-1",
            "type": "invalid_block_type",
            "name": "Invalid",
            "enabled": True,
            "data": {},
        }
    }

    edges = []

    result = await executor.execute(
        workflow_id="test-workflow",
        user_id="test-user",
        blocks=blocks,
        edges=edges,
        input_data={},
    )

    assert result.status == ExecutionStatus.FAILED
    assert len(result.errors) > 0
    assert "No executor found" in result.errors[0]
