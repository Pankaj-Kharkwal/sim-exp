"""Variables block executor - Set and manage workflow variables"""

from typing import Any
from copy import deepcopy

from app.core.logging import get_logger
from app.executor.state import WorkflowState

logger = get_logger(__name__)


async def execute_variables_block(
    block: dict[str, Any], input_data: dict[str, Any], state: WorkflowState
) -> dict[str, Any]:
    """Execute a variables management block

    Supports:
    - Set single variable
    - Set multiple variables
    - Update existing variables
    - Delete variables
    - Get variable values
    """

    logger.info(
        "variables_block_executing",
        block_id=block["id"],
        operation=input_data.get("operation"),
    )

    operation = input_data.get("operation", "set")
    variables_to_set = input_data.get("variables", {})
    variable_name = input_data.get("variable_name")
    variable_value = input_data.get("variable_value")

    if operation == "set":
        # Set single or multiple variables
        if variable_name and variable_value is not None:
            # Set single variable
            state.variables[variable_name] = variable_value
            updated = {variable_name: variable_value}

        elif variables_to_set:
            # Set multiple variables
            state.variables.update(variables_to_set)
            updated = variables_to_set

        else:
            updated = {}

        logger.info(
            "variables_set",
            block_id=block["id"],
            count=len(updated),
        )

        return {
            "operation": "set",
            "updated": updated,
            "all_variables": deepcopy(state.variables),
        }

    elif operation == "delete":
        # Delete variable(s)
        if variable_name:
            # Delete single variable
            deleted = state.variables.pop(variable_name, None)
            deleted_vars = {variable_name: deleted} if deleted is not None else {}

        elif variables_to_set:
            # Delete multiple variables (keys from variables_to_set)
            deleted_vars = {}
            for key in variables_to_set.keys():
                value = state.variables.pop(key, None)
                if value is not None:
                    deleted_vars[key] = value

        else:
            deleted_vars = {}

        logger.info(
            "variables_deleted",
            block_id=block["id"],
            count=len(deleted_vars),
        )

        return {
            "operation": "delete",
            "deleted": deleted_vars,
            "all_variables": deepcopy(state.variables),
        }

    elif operation == "get":
        # Get variable value(s)
        if variable_name:
            # Get single variable
            value = state.variables.get(variable_name)
            retrieved = {variable_name: value}

        elif variables_to_set:
            # Get multiple variables
            retrieved = {
                key: state.variables.get(key)
                for key in variables_to_set.keys()
            }

        else:
            # Get all variables
            retrieved = deepcopy(state.variables)

        return {
            "operation": "get",
            "retrieved": retrieved,
            "all_variables": deepcopy(state.variables),
        }

    elif operation == "clear":
        # Clear all variables
        old_variables = deepcopy(state.variables)
        state.variables.clear()

        logger.info(
            "variables_cleared",
            block_id=block["id"],
            count=len(old_variables),
        )

        return {
            "operation": "clear",
            "cleared": old_variables,
            "all_variables": {},
        }

    else:
        # Unknown operation
        return {
            "operation": operation,
            "error": f"Unknown operation: {operation}",
            "all_variables": deepcopy(state.variables),
        }
