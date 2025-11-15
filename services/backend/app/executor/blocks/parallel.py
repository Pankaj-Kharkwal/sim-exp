"""Parallel block executor - Execute multiple branches concurrently"""

from typing import Any, Optional
import asyncio
from copy import deepcopy

from app.core.logging import get_logger
from app.executor.state import WorkflowState

logger = get_logger(__name__)


class ParallelError(Exception):
    """Custom exception for parallel execution errors"""
    pass


async def execute_parallel_block(
    block: dict[str, Any], input_data: dict[str, Any], state: WorkflowState
) -> dict[str, Any]:
    """Execute multiple workflow branches in parallel

    Supports:
    - Concurrent execution of multiple branches
    - Wait for all branches (default) or first to complete
    - Timeout per branch
    - Error handling strategies (fail_fast, collect_errors, ignore_errors)
    - Result aggregation

    Example:
    {
        "type": "parallel",
        "data": {
            "branches": {
                "fetch_users": {
                    "blocks": {
                        "api_call": {
                            "type": "http",
                            "data": {"url": "https://api.example.com/users"}
                        }
                    }
                },
                "fetch_products": {
                    "blocks": {
                        "api_call": {
                            "type": "http",
                            "data": {"url": "https://api.example.com/products"}
                        }
                    }
                }
            },
            "mode": "all",  # "all" (wait for all) or "race" (first to complete)
            "on_error": "fail_fast",  # "fail_fast", "collect_errors", "ignore_errors"
            "timeout": 30  # Timeout in seconds per branch
        }
    }
    """

    logger.info(
        "parallel_block_executing",
        block_id=block["id"],
        branches_count=len(input_data.get("branches", {})),
    )

    # Extract parallel configuration
    branches = input_data.get("branches", {})
    mode = input_data.get("mode", "all")  # "all" or "race"
    on_error = input_data.get("on_error", "fail_fast")  # "fail_fast", "collect_errors", "ignore_errors"
    timeout = input_data.get("timeout", 300)  # Default 5 minutes per branch
    max_concurrent = input_data.get("max_concurrent")  # Optional: limit concurrent branches

    # Validation
    if not branches:
        raise ParallelError("Parallel block must contain at least one branch")

    if mode not in ["all", "race"]:
        raise ParallelError(f"Invalid mode: {mode}. Must be 'all' or 'race'")

    if on_error not in ["fail_fast", "collect_errors", "ignore_errors"]:
        raise ParallelError(f"Invalid on_error: {on_error}")

    # Execute branches
    async def execute_branch(branch_name: str, branch_config: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        """Execute a single branch"""
        logger.debug(
            "parallel_branch_start",
            block_id=block["id"],
            branch=branch_name,
        )

        try:
            # Create isolated state for this branch
            branch_state = deepcopy(state)
            branch_blocks = branch_config.get("blocks", {})

            if not branch_blocks:
                raise ParallelError(f"Branch '{branch_name}' has no blocks")

            # Import here to avoid circular dependency
            from app.executor.engine import WorkflowExecutor
            from app.executor.variable_resolver import VariableResolver

            executor = WorkflowExecutor()

            # Execute blocks in this branch
            branch_results = {}

            for block_id, block_config in branch_blocks.items():
                block_type = block_config.get("type")
                block_data = block_config.get("data", {})

                # Resolve variables
                resolver = VariableResolver(
                    variables=branch_state.variables,
                    block_outputs=branch_state.block_outputs,
                    input_data=branch_state.input_data,
                )
                resolved_data = resolver.resolve(block_data)

                # Execute block
                block_executor = executor.block_executors.get(block_type)
                if not block_executor:
                    raise ParallelError(f"Unknown block type: {block_type}")

                output = await block_executor(
                    {"id": block_id, "type": block_type},
                    resolved_data,
                    branch_state,
                )

                # Store output
                branch_state.block_outputs[block_id] = output
                branch_results[block_id] = output

            logger.info(
                "parallel_branch_completed",
                block_id=block["id"],
                branch=branch_name,
            )

            return branch_name, {
                "success": True,
                "results": branch_results,
                "error": None,
            }

        except asyncio.TimeoutError:
            logger.error(
                "parallel_branch_timeout",
                block_id=block["id"],
                branch=branch_name,
                timeout=timeout,
            )

            return branch_name, {
                "success": False,
                "results": None,
                "error": f"Branch timed out after {timeout} seconds",
            }

        except Exception as e:
            logger.error(
                "parallel_branch_error",
                block_id=block["id"],
                branch=branch_name,
                error=str(e),
                exc_info=True,
            )

            return branch_name, {
                "success": False,
                "results": None,
                "error": str(e),
            }

    # Create tasks for all branches
    tasks = []

    for branch_name, branch_config in branches.items():
        # Wrap each branch with timeout
        task = asyncio.create_task(
            asyncio.wait_for(
                execute_branch(branch_name, branch_config),
                timeout=timeout,
            )
        )
        tasks.append(task)

    # Execute based on mode
    results = {}
    errors = []
    completed_count = 0
    failed_count = 0

    if mode == "race":
        # Wait for first to complete
        logger.debug(
            "parallel_race_mode",
            block_id=block["id"],
            branches_count=len(tasks),
        )

        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

        # Cancel pending tasks
        for task in pending:
            task.cancel()

        # Get result from completed task
        for task in done:
            try:
                branch_name, result = await task
                results[branch_name] = result

                if result["success"]:
                    completed_count += 1
                else:
                    failed_count += 1
                    errors.append({
                        "branch": branch_name,
                        "error": result["error"],
                    })

            except Exception as e:
                logger.error(
                    "parallel_task_error",
                    block_id=block["id"],
                    error=str(e),
                )

        logger.info(
            "parallel_race_completed",
            block_id=block["id"],
            winner=list(results.keys())[0] if results else None,
        )

    else:  # mode == "all"
        # Wait for all to complete
        logger.debug(
            "parallel_all_mode",
            block_id=block["id"],
            branches_count=len(tasks),
        )

        # Use semaphore if max_concurrent is set
        if max_concurrent:
            semaphore = asyncio.Semaphore(max_concurrent)

            async def limited_execute(branch_name: str, branch_config: dict[str, Any]):
                async with semaphore:
                    return await execute_branch(branch_name, branch_config)

            # Recreate tasks with semaphore
            tasks = []
            for branch_name, branch_config in branches.items():
                task = asyncio.create_task(
                    asyncio.wait_for(
                        limited_execute(branch_name, branch_config),
                        timeout=timeout,
                    )
                )
                tasks.append(task)

        # Execute all tasks
        for coro in asyncio.as_completed(tasks):
            try:
                branch_name, result = await coro
                results[branch_name] = result

                if result["success"]:
                    completed_count += 1
                else:
                    failed_count += 1
                    errors.append({
                        "branch": branch_name,
                        "error": result["error"],
                    })

                    # Handle fail_fast
                    if on_error == "fail_fast":
                        # Cancel remaining tasks
                        for task in tasks:
                            if not task.done():
                                task.cancel()

                        raise ParallelError(
                            f"Branch '{branch_name}' failed: {result['error']}"
                        )

            except asyncio.CancelledError:
                logger.debug(
                    "parallel_task_cancelled",
                    block_id=block["id"],
                )
                continue

            except Exception as e:
                logger.error(
                    "parallel_task_error",
                    block_id=block["id"],
                    error=str(e),
                )

                if on_error == "fail_fast":
                    raise

        logger.info(
            "parallel_all_completed",
            block_id=block["id"],
            completed=completed_count,
            failed=failed_count,
        )

    # Check error handling
    if errors and on_error == "collect_errors":
        logger.warning(
            "parallel_completed_with_errors",
            block_id=block["id"],
            errors_count=len(errors),
        )

    # Return results
    return {
        "success": failed_count == 0 or on_error == "ignore_errors",
        "mode": mode,
        "completed": completed_count,
        "failed": failed_count,
        "total": len(branches),
        "results": results,
        "errors": errors if errors else None,
    }
