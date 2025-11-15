"""Delay block executor - Wait/pause execution"""

import asyncio
from typing import Any
from datetime import datetime

from app.core.logging import get_logger
from app.executor.state import WorkflowState

logger = get_logger(__name__)


async def execute_delay_block(
    block: dict[str, Any], input_data: dict[str, Any], state: WorkflowState
) -> dict[str, Any]:
    """Execute a delay/wait block

    Supports:
    - Delay by seconds
    - Delay by milliseconds
    - Pass-through data
    """

    logger.info(
        "delay_block_executing",
        block_id=block["id"],
        delay_seconds=input_data.get("delay_seconds"),
    )

    # Get delay configuration
    delay_seconds = input_data.get("delay_seconds", 0)
    delay_ms = input_data.get("delay_ms", 0)

    # Calculate total delay
    total_delay = delay_seconds + (delay_ms / 1000.0)

    if total_delay < 0:
        total_delay = 0

    # Maximum delay: 5 minutes
    if total_delay > 300:
        logger.warning(
            "delay_capped",
            block_id=block["id"],
            requested=total_delay,
            capped=300,
        )
        total_delay = 300

    start_time = datetime.utcnow()

    # Perform the delay
    if total_delay > 0:
        await asyncio.sleep(total_delay)

    end_time = datetime.utcnow()
    actual_delay = (end_time - start_time).total_seconds()

    logger.info(
        "delay_block_completed",
        block_id=block["id"],
        requested_delay=total_delay,
        actual_delay=actual_delay,
    )

    # Pass through any input data
    pass_through = input_data.get("pass_through", {})

    return {
        "delayed_seconds": actual_delay,
        "requested_seconds": total_delay,
        "started_at": start_time.isoformat(),
        "ended_at": end_time.isoformat(),
        "pass_through": pass_through,
    }
