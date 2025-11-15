"""
Celery Tasks for Background Processing

Main tasks:
- Workflow execution
- Scheduled workflows
- Notifications
- Data processing
"""

import asyncio
from typing import Any, Dict, Optional
from datetime import datetime
import traceback

from celery import Task
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.logging import get_logger, set_trace_id
from app.core.config import settings
from app.workers.celery_app import celery_app
from app.schemas.workflow import WorkflowExecuteRequest
from app.services.workflow_execution import WorkflowExecutionService

logger = get_logger(__name__)

# Create async engine for workers
async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class AsyncTask(Task):
    """Base task class for async operations"""

    def __call__(self, *args, **kwargs):
        """Run task in asyncio event loop"""
        return asyncio.run(self.run_async(*args, **kwargs))

    async def run_async(self, *args, **kwargs):
        """Override this method in subclasses"""
        raise NotImplementedError


@celery_app.task(
    bind=True,
    name="app.workers.tasks.execute_workflow_task",
    max_retries=3,
    default_retry_delay=60,
)
def execute_workflow_task(
    self,
    workflow_id: str,
    user_id: str,
    input_data: Dict[str, Any],
    trigger_type: str = "manual",
    trace_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Execute a workflow in the background

    Args:
        workflow_id: ID of the workflow to execute
        user_id: ID of the user triggering execution
        input_data: Input data for workflow
        trigger_type: Type of trigger (manual, scheduled, webhook, etc.)
        trace_id: Optional trace ID for logging

    Returns:
        Execution result dictionary
    """

    async def _execute():
        """Inner async function"""
        # Set trace ID for logging
        if trace_id:
            set_trace_id(trace_id)

        logger.info(
            "workflow_execution_task_started",
            workflow_id=workflow_id,
            user_id=user_id,
            task_id=self.request.id,
            trace_id=trace_id,
        )

        try:
            # Create database session
            async with AsyncSessionLocal() as db:
                # Create execution request
                execute_request = WorkflowExecuteRequest(
                    input=input_data,
                    workflow_trigger_type=trigger_type,
                    stream=False,
                )

                # Execute workflow
                execution_service = WorkflowExecutionService()
                response = await execution_service.execute_workflow(
                    workflow_id=workflow_id,
                    user_id=user_id,
                    execute_request=execute_request,
                    db=db,
                )

                logger.info(
                    "workflow_execution_task_completed",
                    workflow_id=workflow_id,
                    execution_id=response.execution_id,
                    success=response.success,
                    task_id=self.request.id,
                )

                return {
                    "success": response.success,
                    "execution_id": response.execution_id,
                    "workflow_id": response.workflow_id,
                    "output": response.output,
                    "task_id": self.request.id,
                }

        except Exception as e:
            logger.error(
                "workflow_execution_task_failed",
                workflow_id=workflow_id,
                error=str(e),
                task_id=self.request.id,
                traceback=traceback.format_exc(),
            )

            # Retry on failure
            if self.request.retries < self.max_retries:
                raise self.retry(exc=e, countdown=60 * (self.request.retries + 1))

            return {
                "success": False,
                "error": str(e),
                "workflow_id": workflow_id,
                "task_id": self.request.id,
            }

    return asyncio.run(_execute())


@celery_app.task(
    bind=True,
    name="app.workers.tasks.schedule_workflow_task",
)
def schedule_workflow_task(
    self,
    workflow_id: str,
    user_id: str,
    schedule_config: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Schedule a workflow for repeated execution

    Args:
        workflow_id: ID of the workflow
        user_id: ID of the user
        schedule_config: Schedule configuration (cron, interval, etc.)

    Returns:
        Schedule confirmation
    """
    logger.info(
        "workflow_schedule_task",
        workflow_id=workflow_id,
        schedule=schedule_config,
        task_id=self.request.id,
    )

    # TODO: Implement workflow scheduling logic
    # This would create periodic tasks using Celery Beat

    return {
        "success": True,
        "workflow_id": workflow_id,
        "schedule": schedule_config,
        "task_id": self.request.id,
    }


@celery_app.task(
    bind=True,
    name="app.workers.tasks.send_notification_task",
    max_retries=5,
    default_retry_delay=30,
)
def send_notification_task(
    self,
    user_id: str,
    notification_type: str,
    data: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Send notification to user

    Args:
        user_id: ID of the user
        notification_type: Type of notification (email, webhook, etc.)
        data: Notification data

    Returns:
        Notification result
    """
    logger.info(
        "notification_task_started",
        user_id=user_id,
        notification_type=notification_type,
        task_id=self.request.id,
    )

    try:
        # TODO: Implement notification sending logic
        # This would integrate with email service, webhook service, etc.

        logger.info(
            "notification_task_completed",
            user_id=user_id,
            notification_type=notification_type,
            task_id=self.request.id,
        )

        return {
            "success": True,
            "user_id": user_id,
            "notification_type": notification_type,
            "task_id": self.request.id,
        }

    except Exception as e:
        logger.error(
            "notification_task_failed",
            user_id=user_id,
            error=str(e),
            task_id=self.request.id,
        )

        # Retry on failure
        if self.request.retries < self.max_retries:
            raise self.retry(exc=e, countdown=30 * (self.request.retries + 1))

        return {
            "success": False,
            "error": str(e),
            "user_id": user_id,
            "task_id": self.request.id,
        }


@celery_app.task(
    bind=True,
    name="app.workers.tasks.process_batch_task",
)
def process_batch_task(
    self,
    workflow_id: str,
    user_id: str,
    items: list[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Process a batch of items through a workflow

    Args:
        workflow_id: ID of the workflow
        user_id: ID of the user
        items: List of items to process

    Returns:
        Batch processing result
    """
    logger.info(
        "batch_processing_task_started",
        workflow_id=workflow_id,
        items_count=len(items),
        task_id=self.request.id,
    )

    results = []
    errors = []

    for idx, item in enumerate(items):
        try:
            # Execute workflow for each item
            result = execute_workflow_task.apply_async(
                args=[workflow_id, user_id, item, "batch"],
                countdown=idx * 2,  # Stagger executions
            )

            results.append({
                "item_index": idx,
                "task_id": result.id,
                "status": "queued",
            })

        except Exception as e:
            logger.error(
                "batch_item_failed",
                workflow_id=workflow_id,
                item_index=idx,
                error=str(e),
            )
            errors.append({
                "item_index": idx,
                "error": str(e),
            })

    logger.info(
        "batch_processing_task_completed",
        workflow_id=workflow_id,
        items_processed=len(results),
        errors_count=len(errors),
        task_id=self.request.id,
    )

    return {
        "success": True,
        "workflow_id": workflow_id,
        "items_count": len(items),
        "results": results,
        "errors": errors,
        "task_id": self.request.id,
    }


@celery_app.task(
    bind=True,
    name="app.workers.tasks.cleanup_old_logs_task",
)
def cleanup_old_logs_task(
    self,
    days_old: int = 30,
) -> Dict[str, Any]:
    """
    Cleanup old execution logs

    Args:
        days_old: Number of days to keep logs

    Returns:
        Cleanup result
    """

    async def _cleanup():
        """Inner async function"""
        from datetime import timedelta
        from sqlalchemy import delete
        from app.db.models.workflow import WorkflowExecutionLog

        logger.info(
            "cleanup_logs_task_started",
            days_old=days_old,
            task_id=self.request.id,
        )

        try:
            async with AsyncSessionLocal() as db:
                # Calculate cutoff date
                cutoff_date = datetime.utcnow() - timedelta(days=days_old)

                # Delete old logs
                result = await db.execute(
                    delete(WorkflowExecutionLog).where(
                        WorkflowExecutionLog.created_at < cutoff_date
                    )
                )

                await db.commit()

                deleted_count = result.rowcount

                logger.info(
                    "cleanup_logs_task_completed",
                    deleted_count=deleted_count,
                    task_id=self.request.id,
                )

                return {
                    "success": True,
                    "deleted_count": deleted_count,
                    "task_id": self.request.id,
                }

        except Exception as e:
            logger.error(
                "cleanup_logs_task_failed",
                error=str(e),
                task_id=self.request.id,
            )
            return {
                "success": False,
                "error": str(e),
                "task_id": self.request.id,
            }

    return asyncio.run(_cleanup())
