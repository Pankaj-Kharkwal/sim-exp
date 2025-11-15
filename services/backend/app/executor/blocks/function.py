"""Function block executor - JavaScript/Python code execution"""

from typing import Any
import json

from app.core.logging import get_logger
from app.executor.state import WorkflowState

logger = get_logger(__name__)


async def execute_function_block(
    block: dict[str, Any], input_data: dict[str, Any], state: WorkflowState
) -> dict[str, Any]:
    """Execute a custom function block

    Note: For prototype, we'll use limited Python eval.
    In production, use sandboxed execution (E2B, etc.)
    """

    logger.info("function_block_executing", block_id=block["id"])

    code = input_data.get("code", "")

    if not code:
        raise ValueError("Code is required for function block")

    # For prototype: Very limited and unsafe - only for demo!
    # TODO: Replace with sandboxed execution (E2B Code Interpreter)

    # Create execution context with inputs
    context = {
        "input": state.input_data,
        "variables": state.variables,
        "json": json,
        # Add more safe utilities as needed
    }

    # Add outputs from previous blocks
    for block_id, output in state.block_outputs.items():
        context[block_id] = output

    try:
        # Execute code (UNSAFE - for prototype only!)
        result = eval(code, {"__builtins__": {}}, context)

        logger.info("function_block_completed", block_id=block["id"])

        return {"result": result, "success": True}

    except Exception as e:
        logger.error("function_block_failed", block_id=block["id"], error=str(e))
        return {"error": str(e), "success": False}
