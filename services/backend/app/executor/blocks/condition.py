"""Condition block executor - Conditional branching"""

from typing import Any

from app.core.logging import get_logger
from app.executor.state import WorkflowState

logger = get_logger(__name__)


async def execute_condition_block(
    block: dict[str, Any], input_data: dict[str, Any], state: WorkflowState
) -> dict[str, Any]:
    """Execute a condition block for branching logic"""

    logger.info("condition_block_executing", block_id=block["id"])

    expression = input_data.get("expression", "true")

    # Simple expression evaluation
    # TODO: Enhance with proper expression parser

    try:
        # Create evaluation context
        context = {
            "input": state.input_data,
            "variables": state.variables,
        }

        # Add outputs from previous blocks
        for block_id, output in state.block_outputs.items():
            context[block_id] = output

        # Evaluate expression (UNSAFE - for prototype only!)
        result = eval(expression, {"__builtins__": {}}, context)

        logger.info(
            "condition_block_completed",
            block_id=block["id"],
            result=bool(result),
        )

        return {"condition": bool(result), "expression": expression}

    except Exception as e:
        logger.error(
            "condition_block_failed",
            block_id=block["id"],
            error=str(e),
        )
        return {"condition": False, "error": str(e)}
