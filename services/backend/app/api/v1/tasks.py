"""
Task Management API Endpoints

Endpoints for:
- Querying task status
- Cancelling tasks
- Listing active tasks
- Task statistics
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, status

from app.core.logging import get_logger
from app.workers.celery_app import celery_app
from celery.result import AsyncResult

router = APIRouter()
logger = get_logger(__name__)


@router.get("/")
async def list_tasks(
    limit: int = 100,
    queue: Optional[str] = None,
):
    """
    List active tasks

    - **limit**: Maximum number of tasks to return
    - **queue**: Filter by queue name (optional)
    """
    logger.info("list_tasks", limit=limit, queue=queue)

    try:
        # Get active tasks from Celery
        inspect = celery_app.control.inspect()

        active_tasks = inspect.active() or {}
        scheduled_tasks = inspect.scheduled() or {}
        reserved_tasks = inspect.reserved() or {}

        # Combine all tasks
        all_tasks = []

        for worker, tasks in active_tasks.items():
            for task in tasks[:limit]:
                all_tasks.append({
                    "id": task["id"],
                    "name": task["name"],
                    "args": task["args"],
                    "kwargs": task["kwargs"],
                    "worker": worker,
                    "status": "active",
                })

        for worker, tasks in scheduled_tasks.items():
            for task in tasks[:limit]:
                all_tasks.append({
                    "id": task["request"]["id"],
                    "name": task["request"]["name"],
                    "worker": worker,
                    "status": "scheduled",
                    "eta": task["eta"],
                })

        return {
            "tasks": all_tasks[:limit],
            "total": len(all_tasks),
        }

    except Exception as e:
        logger.error("list_tasks_error", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list tasks: {str(e)}",
        )


@router.get("/{task_id}")
async def get_task_status(task_id: str):
    """
    Get task status by ID

    Returns:
    - Task state (PENDING, STARTED, SUCCESS, FAILURE, RETRY, REVOKED)
    - Result (if completed)
    - Error information (if failed)
    """
    logger.info("get_task_status", task_id=task_id)

    try:
        # Get task result
        result = AsyncResult(task_id, app=celery_app)

        response = {
            "task_id": task_id,
            "state": result.state,
            "ready": result.ready(),
            "successful": result.successful() if result.ready() else None,
            "failed": result.failed() if result.ready() else None,
        }

        # Add result or error info
        if result.ready():
            if result.successful():
                response["result"] = result.result
            elif result.failed():
                response["error"] = str(result.info)
                response["traceback"] = result.traceback

        # Add task info if available
        if result.info:
            response["info"] = result.info

        return response

    except Exception as e:
        logger.error("get_task_status_error", task_id=task_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get task status: {str(e)}",
        )


@router.post("/{task_id}/cancel")
async def cancel_task(task_id: str):
    """
    Cancel a running or pending task

    Sends revoke signal to Celery worker.
    """
    logger.info("cancel_task", task_id=task_id)

    try:
        # Revoke task
        celery_app.control.revoke(task_id, terminate=True)

        logger.info("cancel_task_success", task_id=task_id)

        return {
            "success": True,
            "task_id": task_id,
            "message": "Task cancellation requested",
        }

    except Exception as e:
        logger.error("cancel_task_error", task_id=task_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to cancel task: {str(e)}",
        )


@router.get("/stats/workers")
async def get_worker_stats():
    """
    Get statistics about Celery workers

    Returns:
    - Number of active workers
    - Worker names and status
    - Task counts per worker
    """
    logger.info("get_worker_stats")

    try:
        inspect = celery_app.control.inspect()

        stats = inspect.stats() or {}
        active = inspect.active() or {}
        registered = inspect.registered() or {}

        workers = []

        for worker_name, worker_stats in stats.items():
            workers.append({
                "name": worker_name,
                "status": "online",
                "pool": worker_stats.get("pool", {}),
                "active_tasks": len(active.get(worker_name, [])),
                "registered_tasks": len(registered.get(worker_name, [])),
            })

        return {
            "workers": workers,
            "total_workers": len(workers),
        }

    except Exception as e:
        logger.error("get_worker_stats_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get worker stats: {str(e)}",
        )


@router.get("/stats/queues")
async def get_queue_stats():
    """
    Get statistics about task queues

    Returns:
    - Queue names
    - Number of tasks in each queue
    """
    logger.info("get_queue_stats")

    try:
        inspect = celery_app.control.inspect()

        active_queues = inspect.active_queues() or {}

        queues = []

        for worker, worker_queues in active_queues.items():
            for queue in worker_queues:
                queues.append({
                    "name": queue["name"],
                    "exchange": queue.get("exchange", {}).get("name"),
                    "routing_key": queue["routing_key"],
                    "worker": worker,
                })

        return {
            "queues": queues,
            "total_queues": len(set(q["name"] for q in queues)),
        }

    except Exception as e:
        logger.error("get_queue_stats_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get queue stats: {str(e)}",
        )


@router.post("/test")
async def test_task():
    """
    Test task endpoint - queues a debug task

    Useful for testing that Celery workers are running correctly.
    """
    logger.info("test_task_requested")

    try:
        from app.workers.celery_app import debug_task

        # Queue debug task
        result = debug_task.delay()

        return {
            "success": True,
            "task_id": result.id,
            "message": "Debug task queued successfully",
        }

    except Exception as e:
        logger.error("test_task_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to queue test task: {str(e)}",
        )
