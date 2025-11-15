"""Loop block executor - Iterate over arrays and execute sub-workflows"""

from typing import Any, Optional
import asyncio
from copy import deepcopy

from app.core.logging import get_logger
from app.executor.state import WorkflowState

logger = get_logger(__name__)


class LoopError(Exception):
    """Custom exception for loop errors"""
    pass


async def execute_loop_block(
    block: dict[str, Any], input_data: dict[str, Any], state: WorkflowState
) -> dict[str, Any]:
    """Execute a loop block to iterate over arrays

    Supports:
    - Array iteration with index tracking
    - Current item access via {{loop.item}}
    - Current index access via {{loop.index}}
    - Break on condition
    - Max iteration limits
    - Collect results from each iteration

    Example:
    {
        "type": "loop",
        "data": {
            "items": [1, 2, 3, 4, 5],
            "variable_name": "current_item",  # Optional: defaults to "loop.item"
            "max_iterations": 100,
            "break_on": "{{output.error}}",  # Optional: condition to break early
            "blocks": {
                "process": {
                    "type": "transformer",
                    "data": {
                        "operation": "multiply",
                        "data": "{{current_item}}",
                        "multiplier": 2
                    }
                }
            }
        }
    }
    """

    logger.info(
        "loop_block_executing",
        block_id=block["id"],
        items_count=len(input_data.get("items", [])),
    )

    # Extract loop configuration
    items = input_data.get("items", [])
    variable_name = input_data.get("variable_name", "loop_item")
    index_name = input_data.get("index_name", "loop_index")
    max_iterations = input_data.get("max_iterations", 10000)
    break_on = input_data.get("break_on")
    collect_results = input_data.get("collect_results", True)
    blocks = input_data.get("blocks", {})

    # Validation
    if not isinstance(items, list):
        raise LoopError(f"Items must be a list, got {type(items).__name__}")

    if not blocks:
        raise LoopError("Loop must contain at least one block to execute")

    if len(items) > max_iterations:
        logger.warning(
            "loop_items_truncated",
            block_id=block["id"],
            items_count=len(items),
            max_iterations=max_iterations,
        )
        items = items[:max_iterations]

    # Execute loop
    results = []
    iterations = 0
    broke_early = False

    for index, item in enumerate(items):
        iterations += 1

        logger.debug(
            "loop_iteration_start",
            block_id=block["id"],
            iteration=iterations,
            index=index,
        )

        # Set loop variables in state
        loop_state = deepcopy(state)
        loop_state.variables[variable_name] = item
        loop_state.variables[index_name] = index
        loop_state.variables["loop"] = {
            "item": item,
            "index": index,
            "total": len(items),
            "is_first": index == 0,
            "is_last": index == len(items) - 1,
        }

        # Execute blocks for this iteration
        iteration_result = {}

        try:
            # Import here to avoid circular dependency
            from app.executor.engine import WorkflowExecutor

            executor = WorkflowExecutor()

            # Execute each block in the loop body
            for block_id, block_config in blocks.items():
                block_type = block_config.get("type")
                block_data = block_config.get("data", {})

                # Resolve variables in block data
                from app.executor.variable_resolver import VariableResolver
                resolver = VariableResolver(
                    variables=loop_state.variables,
                    block_outputs=loop_state.block_outputs,
                    input_data=loop_state.input_data,
                )
                resolved_data = resolver.resolve(block_data)

                # Execute block
                block_executor = executor.block_executors.get(block_type)
                if not block_executor:
                    raise LoopError(f"Unknown block type: {block_type}")

                output = await block_executor(
                    {"id": block_id, "type": block_type},
                    resolved_data,
                    loop_state,
                )

                # Store output
                loop_state.block_outputs[block_id] = output
                iteration_result[block_id] = output

            # Check break condition
            if break_on:
                resolver = VariableResolver(
                    variables=loop_state.variables,
                    block_outputs=loop_state.block_outputs,
                    input_data=loop_state.input_data,
                )
                should_break = resolver.resolve(break_on)

                if should_break:
                    logger.info(
                        "loop_break_condition_met",
                        block_id=block["id"],
                        iteration=iterations,
                    )
                    broke_early = True
                    if collect_results:
                        results.append({
                            "index": index,
                            "item": item,
                            "output": iteration_result,
                        })
                    break

            # Collect results
            if collect_results:
                results.append({
                    "index": index,
                    "item": item,
                    "output": iteration_result,
                })

        except Exception as e:
            logger.error(
                "loop_iteration_error",
                block_id=block["id"],
                iteration=iterations,
                index=index,
                error=str(e),
                exc_info=True,
            )

            # Decide whether to continue or break on error
            on_error = input_data.get("on_error", "break")

            if on_error == "continue":
                # Add error result and continue
                if collect_results:
                    results.append({
                        "index": index,
                        "item": item,
                        "error": str(e),
                    })
                continue
            else:
                # Break on error
                raise LoopError(f"Loop failed at iteration {iterations}: {str(e)}") from e

    logger.info(
        "loop_block_completed",
        block_id=block["id"],
        iterations=iterations,
        broke_early=broke_early,
    )

    return {
        "success": True,
        "iterations": iterations,
        "broke_early": broke_early,
        "results": results,
        "total_items": len(items),
    }
