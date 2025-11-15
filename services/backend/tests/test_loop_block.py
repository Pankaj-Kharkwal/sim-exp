"""Tests for loop block"""

import pytest
from app.executor.blocks.loop import execute_loop_block
from app.executor.state import WorkflowState


@pytest.mark.asyncio
async def test_loop_simple_iteration():
    """Test basic loop iteration"""

    state = WorkflowState(
        execution_id="test",
        workflow_id="test",
        user_id="test",
        trace_id="test",
        input_data={},
        blocks={},
        edges=[],
    )

    block = {
        "id": "loop1",
        "type": "loop",
    }

    input_data = {
        "items": [1, 2, 3, 4, 5],
        "variable_name": "current_number",
        "blocks": {
            "multiply": {
                "type": "transformer",
                "data": {
                    "operation": "identity",
                    "data": "{{current_number}}",
                }
            }
        }
    }

    result = await execute_loop_block(block, input_data, state)

    assert result["success"] is True
    assert result["iterations"] == 5
    assert result["broke_early"] is False
    assert len(result["results"]) == 5


@pytest.mark.asyncio
async def test_loop_with_index():
    """Test loop with index tracking"""

    state = WorkflowState(
        execution_id="test",
        workflow_id="test",
        user_id="test",
        trace_id="test",
        input_data={},
        blocks={},
        edges=[],
    )

    block = {
        "id": "loop1",
        "type": "loop",
    }

    input_data = {
        "items": ["a", "b", "c"],
        "variable_name": "item",
        "index_name": "idx",
        "blocks": {
            "process": {
                "type": "variables",
                "data": {
                    "operation": "set",
                    "variable_name": "test",
                    "variable_value": "{{idx}}",
                }
            }
        }
    }

    result = await execute_loop_block(block, input_data, state)

    assert result["success"] is True
    assert result["iterations"] == 3
    # Check that loop variables were set correctly
    assert result["results"][0]["index"] == 0
    assert result["results"][1]["index"] == 1
    assert result["results"][2]["index"] == 2


@pytest.mark.asyncio
async def test_loop_max_iterations():
    """Test max iterations limit"""

    state = WorkflowState(
        execution_id="test",
        workflow_id="test",
        user_id="test",
        trace_id="test",
        input_data={},
        blocks={},
        edges=[],
    )

    block = {
        "id": "loop1",
        "type": "loop",
    }

    input_data = {
        "items": list(range(100)),
        "max_iterations": 10,
        "blocks": {
            "process": {
                "type": "variables",
                "data": {
                    "operation": "set",
                    "variable_name": "test",
                    "variable_value": "{{loop_item}}",
                }
            }
        }
    }

    result = await execute_loop_block(block, input_data, state)

    assert result["success"] is True
    assert result["iterations"] == 10  # Should be limited to max_iterations


@pytest.mark.asyncio
async def test_loop_break_condition():
    """Test loop with break condition"""

    state = WorkflowState(
        execution_id="test",
        workflow_id="test",
        user_id="test",
        trace_id="test",
        input_data={},
        blocks={},
        edges=[],
    )

    state.variables["stop_value"] = 3

    block = {
        "id": "loop1",
        "type": "loop",
    }

    input_data = {
        "items": [1, 2, 3, 4, 5],
        "variable_name": "num",
        "break_on": "{{num}} >= {{stop_value}}",
        "blocks": {
            "process": {
                "type": "variables",
                "data": {
                    "operation": "set",
                    "variable_name": "current",
                    "variable_value": "{{num}}",
                }
            }
        }
    }

    result = await execute_loop_block(block, input_data, state)

    assert result["broke_early"] is True
    assert result["iterations"] <= 3  # Should break at or before value 3


@pytest.mark.asyncio
async def test_loop_empty_array():
    """Test loop with empty array"""

    state = WorkflowState(
        execution_id="test",
        workflow_id="test",
        user_id="test",
        trace_id="test",
        input_data={},
        blocks={},
        edges=[],
    )

    block = {
        "id": "loop1",
        "type": "loop",
    }

    input_data = {
        "items": [],
        "blocks": {
            "process": {
                "type": "variables",
                "data": {
                    "operation": "set",
                    "variable_name": "test",
                    "variable_value": "value",
                }
            }
        }
    }

    result = await execute_loop_block(block, input_data, state)

    assert result["success"] is True
    assert result["iterations"] == 0
    assert len(result["results"]) == 0


@pytest.mark.asyncio
async def test_loop_invalid_items():
    """Test loop with invalid items (not an array)"""

    state = WorkflowState(
        execution_id="test",
        workflow_id="test",
        user_id="test",
        trace_id="test",
        input_data={},
        blocks={},
        edges=[],
    )

    block = {
        "id": "loop1",
        "type": "loop",
    }

    input_data = {
        "items": "not an array",
        "blocks": {
            "process": {
                "type": "variables",
                "data": {
                    "operation": "set",
                    "variable_name": "test",
                    "variable_value": "value",
                }
            }
        }
    }

    with pytest.raises(Exception):  # Should raise LoopError
        await execute_loop_block(block, input_data, state)


@pytest.mark.asyncio
async def test_loop_no_blocks():
    """Test loop with no blocks to execute"""

    state = WorkflowState(
        execution_id="test",
        workflow_id="test",
        user_id="test",
        trace_id="test",
        input_data={},
        blocks={},
        edges=[],
    )

    block = {
        "id": "loop1",
        "type": "loop",
    }

    input_data = {
        "items": [1, 2, 3],
        "blocks": {}
    }

    with pytest.raises(Exception):  # Should raise LoopError
        await execute_loop_block(block, input_data, state)


@pytest.mark.asyncio
async def test_loop_collect_results_disabled():
    """Test loop with result collection disabled"""

    state = WorkflowState(
        execution_id="test",
        workflow_id="test",
        user_id="test",
        trace_id="test",
        input_data={},
        blocks={},
        edges=[],
    )

    block = {
        "id": "loop1",
        "type": "loop",
    }

    input_data = {
        "items": [1, 2, 3],
        "collect_results": False,
        "blocks": {
            "process": {
                "type": "variables",
                "data": {
                    "operation": "set",
                    "variable_name": "test",
                    "variable_value": "{{loop_item}}",
                }
            }
        }
    }

    result = await execute_loop_block(block, input_data, state)

    assert result["success"] is True
    assert result["iterations"] == 3
    assert len(result["results"]) == 0  # Results not collected
