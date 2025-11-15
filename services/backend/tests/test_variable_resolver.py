"""Test variable resolution"""

import pytest
import os
from datetime import datetime

from app.executor.variable_resolver import VariableResolver, resolve_variables
from app.executor.state import WorkflowState, ExecutionStatus


@pytest.fixture
def mock_state():
    """Create a mock workflow state for testing"""
    state = WorkflowState(
        execution_id="test-exec",
        workflow_id="test-workflow",
        user_id="test-user",
        trace_id="test-trace",
        input_data={"name": "John", "age": 30, "nested": {"city": "NYC"}},
        blocks={},
        edges=[],
        variables={"api_url": "https://api.example.com", "timeout": 60},
        status=ExecutionStatus.RUNNING,
        started_at=datetime.utcnow(),
    )

    # Add some block outputs
    state.set_block_output("block-1", {"result": "success", "count": 42})
    state.set_block_output("block-2", {"items": ["a", "b", "c"], "total": 3})
    state.set_block_output(
        "block-3",
        {"data": {"user": {"name": "Alice", "email": "alice@example.com"}}},
    )

    return state


def test_simple_variable_resolution(mock_state):
    """Test resolving simple workflow variables"""
    resolver = VariableResolver(mock_state)

    assert resolver.resolve("{{api_url}}") == "https://api.example.com"
    assert resolver.resolve("{{timeout}}") == 60
    assert resolver.resolve("{{variables.api_url}}") == "https://api.example.com"
    assert resolver.resolve("{{var.timeout}}") == 60


def test_input_variable_resolution(mock_state):
    """Test resolving input variables"""
    resolver = VariableResolver(mock_state)

    assert resolver.resolve("{{input.name}}") == "John"
    assert resolver.resolve("{{input.age}}") == 30
    assert resolver.resolve("{{input.nested.city}}") == "NYC"


def test_block_output_resolution(mock_state):
    """Test resolving block outputs"""
    resolver = VariableResolver(mock_state)

    assert resolver.resolve("{{block-1.output.result}}") == "success"
    assert resolver.resolve("{{block-1.output.count}}") == 42
    assert resolver.resolve("{{block-2.output.total}}") == 3


def test_nested_block_output_resolution(mock_state):
    """Test resolving nested block outputs"""
    resolver = VariableResolver(mock_state)

    result = resolver.resolve("{{block-3.output.data.user.name}}")
    assert result == "Alice"

    result = resolver.resolve("{{block-3.output.data.user.email}}")
    assert result == "alice@example.com"


def test_array_access_in_block_output(mock_state):
    """Test array indexing in block outputs"""
    resolver = VariableResolver(mock_state)

    assert resolver.resolve("{{block-2.output.items.0}}") == "a"
    assert resolver.resolve("{{block-2.output.items.1}}") == "b"
    assert resolver.resolve("{{block-2.output.items.2}}") == "c"


def test_variable_in_string(mock_state):
    """Test variable substitution within strings"""
    resolver = VariableResolver(mock_state)

    result = resolver.resolve("Hello {{input.name}}, you are {{input.age}} years old")
    assert result == "Hello John, you are 30 years old"

    result = resolver.resolve("API: {{api_url}}/endpoint")
    assert result == "API: https://api.example.com/endpoint"


def test_multiple_variables_in_string(mock_state):
    """Test multiple variables in one string"""
    resolver = VariableResolver(mock_state)

    result = resolver.resolve(
        "User {{input.name}} from {{input.nested.city}}, result: {{block-1.output.result}}"
    )
    assert result == "User John from NYC, result: success"


def test_dict_with_variables(mock_state):
    """Test resolving variables in dictionaries"""
    resolver = VariableResolver(mock_state)

    data = {
        "url": "{{api_url}}",
        "timeout": "{{timeout}}",
        "user": "{{input.name}}",
        "count": "{{block-1.output.count}}",
    }

    result = resolver.resolve(data)

    assert result["url"] == "https://api.example.com"
    assert result["timeout"] == 60
    assert result["user"] == "John"
    assert result["count"] == 42


def test_list_with_variables(mock_state):
    """Test resolving variables in lists"""
    resolver = VariableResolver(mock_state)

    data = [
        "{{input.name}}",
        "{{input.age}}",
        "{{block-1.output.result}}",
        "Static text",
    ]

    result = resolver.resolve(data)

    assert result == ["John", 30, "success", "Static text"]


def test_nested_structures(mock_state):
    """Test resolving variables in nested structures"""
    resolver = VariableResolver(mock_state)

    data = {
        "user": {
            "name": "{{input.name}}",
            "details": {"age": "{{input.age}}", "city": "{{input.nested.city}}"},
        },
        "results": ["{{block-1.output.result}}", "{{block-2.output.total}}"],
    }

    result = resolver.resolve(data)

    assert result["user"]["name"] == "John"
    assert result["user"]["details"]["age"] == 30
    assert result["user"]["details"]["city"] == "NYC"
    assert result["results"] == ["success", 3]


def test_env_variable_resolution(mock_state):
    """Test resolving environment variables"""
    # Set a test environment variable
    os.environ["TEST_API_KEY"] = "secret-key-123"
    os.environ["TEST_URL"] = "https://test.example.com"

    resolver = VariableResolver(mock_state)

    assert resolver.resolve("{{env.TEST_API_KEY}}") == "secret-key-123"
    assert resolver.resolve("{{env.TEST_URL}}") == "https://test.example.com"

    # Clean up
    del os.environ["TEST_API_KEY"]
    del os.environ["TEST_URL"]


def test_missing_variable(mock_state):
    """Test handling of missing variables"""
    resolver = VariableResolver(mock_state)

    # Missing workflow variable
    result = resolver.resolve("{{missing_var}}")
    assert result == "{{missing_var}}"  # Unchanged

    # Missing input field
    result = resolver.resolve("{{input.missing}}")
    assert result == "{{input.missing}}"

    # Missing block output
    result = resolver.resolve("{{missing-block.output}}")
    assert result == "{{missing-block.output}}"


def test_non_string_values(mock_state):
    """Test that non-string values are passed through"""
    resolver = VariableResolver(mock_state)

    assert resolver.resolve(42) == 42
    assert resolver.resolve(3.14) == 3.14
    assert resolver.resolve(True) is True
    assert resolver.resolve(None) is None


def test_convenience_function(mock_state):
    """Test the convenience resolve_variables function"""
    data = {
        "name": "{{input.name}}",
        "result": "{{block-1.output.result}}",
    }

    result = resolve_variables(data, mock_state)

    assert result["name"] == "John"
    assert result["result"] == "success"


def test_shorthand_block_reference(mock_state):
    """Test shorthand block reference without .output"""
    resolver = VariableResolver(mock_state)

    # Should work with or without .output
    assert resolver.resolve("{{block-1.result}}") == "success"
    assert resolver.resolve("{{block-1.count}}") == 42


def test_entire_object_resolution(mock_state):
    """Test returning entire objects when no field specified"""
    resolver = VariableResolver(mock_state)

    result = resolver.resolve("{{block-1.output}}")
    assert result == {"result": "success", "count": 42}

    result = resolver.resolve("{{block-2.output}}")
    assert result == {"items": ["a", "b", "c"], "total": 3}
