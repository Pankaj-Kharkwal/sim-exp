"""Variable resolution for workflow execution

Supports:
- {{variable_name}} - Workflow variables
- {{block_id.output}} - Block output references
- {{block_id.output.field}} - Nested field access
- {{env.VAR_NAME}} - Environment variables
- {{input.field}} - Workflow input data
"""

import re
from typing import Any, Optional
import os

from app.core.logging import get_logger
from app.executor.state import WorkflowState

logger = get_logger(__name__)

# Regex pattern to match {{variable}} syntax
VARIABLE_PATTERN = re.compile(r'\{\{([^}]+)\}\}')


class VariableResolver:
    """Resolves variables in workflow execution"""

    def __init__(self, state: WorkflowState):
        self.state = state

    def resolve(self, value: Any) -> Any:
        """Resolve variables in any type of value"""
        if isinstance(value, str):
            return self._resolve_string(value)
        elif isinstance(value, dict):
            return {k: self.resolve(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [self.resolve(item) for item in value]
        else:
            return value

    def _resolve_string(self, text: str) -> Any:
        """Resolve variables in a string

        If the entire string is a single variable, return the actual value.
        Otherwise, replace variables within the string.
        """
        # Check if entire string is a single variable
        if text.startswith('{{') and text.endswith('}}') and text.count('{{') == 1:
            var_name = text[2:-2].strip()
            resolved = self._resolve_variable(var_name)
            if resolved is not None:
                return resolved

        # Replace all variables in the string
        def replace_match(match):
            var_name = match.group(1).strip()
            resolved = self._resolve_variable(var_name)
            return str(resolved) if resolved is not None else match.group(0)

        return VARIABLE_PATTERN.sub(replace_match, text)

    def _resolve_variable(self, var_name: str) -> Any:
        """Resolve a single variable reference"""
        parts = var_name.split('.')

        # Check for special prefixes
        if parts[0] == 'env':
            # Environment variable: {{env.API_KEY}}
            return self._resolve_env_var(parts[1:])

        elif parts[0] == 'input':
            # Workflow input: {{input.field}}
            return self._resolve_input(parts[1:])

        elif parts[0] == 'variables' or parts[0] == 'var':
            # Workflow variables: {{variables.name}} or {{var.name}}
            return self._resolve_workflow_variable(parts[1:])

        elif len(parts) >= 2 and parts[1] in ['output', 'result']:
            # Block output: {{block_id.output.field}}
            return self._resolve_block_output(parts[0], parts[2:])

        else:
            # Try as workflow variable first
            result = self._resolve_workflow_variable(parts)
            if result is not None:
                return result

            # Try as block ID
            if len(parts) >= 1:
                return self._resolve_block_output(parts[0], parts[1:])

        logger.warning("variable_not_found", variable=var_name)
        return None

    def _resolve_env_var(self, path: list[str]) -> Optional[str]:
        """Resolve environment variable"""
        if not path:
            return None

        env_var_name = path[0].upper()
        value = os.getenv(env_var_name)

        if value is None:
            logger.warning("env_var_not_found", variable=env_var_name)
            return None

        # Support nested access for JSON env vars (future)
        if len(path) > 1:
            logger.warning("nested_env_vars_not_supported", variable=env_var_name)

        return value

    def _resolve_input(self, path: list[str]) -> Any:
        """Resolve workflow input field"""
        result = self.state.input_data

        for key in path:
            if isinstance(result, dict):
                result = result.get(key)
                if result is None:
                    return None
            else:
                return None

        return result

    def _resolve_workflow_variable(self, path: list[str]) -> Any:
        """Resolve workflow-level variable"""
        if not path:
            return None

        result = self.state.variables

        for key in path:
            if isinstance(result, dict):
                result = result.get(key)
                if result is None:
                    return None
            else:
                return None

        return result

    def _resolve_block_output(self, block_id: str, path: list[str]) -> Any:
        """Resolve block output field"""
        # Get block output from state
        block_output = self.state.get_block_output(block_id)

        if block_output is None:
            logger.warning("block_output_not_found", block_id=block_id)
            return None

        # If no path specified, return entire output
        if not path or (len(path) == 1 and path[0] == ''):
            return block_output

        # Navigate through nested fields
        result = block_output
        for key in path:
            if isinstance(result, dict):
                result = result.get(key)
                if result is None:
                    logger.warning(
                        "block_output_field_not_found",
                        block_id=block_id,
                        field='.'.join(path),
                    )
                    return None
            elif isinstance(result, list) and key.isdigit():
                # Support array indexing: {{block.output.0}}
                idx = int(key)
                if 0 <= idx < len(result):
                    result = result[idx]
                else:
                    return None
            else:
                return None

        return result


def resolve_variables(data: Any, state: WorkflowState) -> Any:
    """Convenience function to resolve variables in data"""
    resolver = VariableResolver(state)
    return resolver.resolve(data)
