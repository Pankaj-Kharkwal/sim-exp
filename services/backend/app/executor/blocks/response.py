"""Response block executor - Final output"""

from typing import Any

from app.core.logging import get_logger
from app.executor.state import WorkflowState

logger = get_logger(__name__)


async def execute_response_block(
    block: dict[str, Any], input_data: dict[str, Any], state: WorkflowState
) -> dict[str, Any]:
    """Execute a response block - formats final workflow output"""

    logger.info("response_block_executing", block_id=block["id"])

    # Extract data to return
    response_data = input_data.get("data", {})
    status = input_data.get("status", 200)

    # Resolve any variables in the response
    resolved_data = {}
    for key, value in response_data.items():
        if isinstance(value, str):
            resolved_data[key] = state.resolve_variable(value)
        else:
            resolved_data[key] = value

    # Store as final output
    state.output_data = resolved_data

    logger.info("response_block_completed", block_id=block["id"])

    return {"data": resolved_data, "status": status}
