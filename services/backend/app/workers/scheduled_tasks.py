"""
Scheduled Celery Tasks

Periodic tasks that run on schedule:
- Cleanup tasks
- Summary reports
- Health checks
- Maintenance operations
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any

from sqlalchemy import delete, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.workers.celery_app import celery_app
from app.workers.tasks import AsyncSessionLocal
from app.db.models.workflow import (
    WorkflowExecutionLog,
    WorkflowExecutionSnapshot,
)

logger = get_logger(__name__)


@celery_app.task(name="app.workers.scheduled_tasks.cleanup_old_logs_task")
def cleanup_old_logs_task(days_old: int = 30) -> Dict[str, Any]:
    """
    Cleanup execution logs older than specified days

    Runs daily at 2 AM
    """

    async def _cleanup():
        logger.info("scheduled_cleanup_logs_started", days_old=days_old)

        try:
            async with AsyncSessionLocal() as db:
                cutoff_date = datetime.utcnow() - timedelta(days=days_old)

                # Delete old logs
                result = await db.execute(
                    delete(WorkflowExecutionLog).where(
                        WorkflowExecutionLog.started_at < cutoff_date
                    )
                )

                await db.commit()

                deleted_count = result.rowcount

                logger.info(
                    "scheduled_cleanup_logs_completed",
                    deleted_count=deleted_count,
                    days_old=days_old,
                )

                return {
                    "success": True,
                    "deleted_count": deleted_count,
                    "days_old": days_old,
                }

        except Exception as e:
            logger.error(
                "scheduled_cleanup_logs_failed",
                error=str(e),
                exc_info=True,
            )
            return {
                "success": False,
                "error": str(e),
            }

    return asyncio.run(_cleanup())


@celery_app.task(name="app.workers.scheduled_tasks.cleanup_old_executions_task")
def cleanup_old_executions_task(days_old: int = 90) -> Dict[str, Any]:
    """
    Cleanup very old execution records

    Runs daily at 3 AM
    """

    async def _cleanup():
        logger.info("scheduled_cleanup_executions_started", days_old=days_old)

        try:
            async with AsyncSessionLocal() as db:
                cutoff_date = datetime.utcnow() - timedelta(days=days_old)

                # Delete old execution logs with failed status
                result = await db.execute(
                    delete(WorkflowExecutionLog).where(
                        WorkflowExecutionLog.started_at < cutoff_date,
                        WorkflowExecutionLog.status == "failed",
                    )
                )

                await db.commit()

                deleted_count = result.rowcount

                logger.info(
                    "scheduled_cleanup_executions_completed",
                    deleted_count=deleted_count,
                    days_old=days_old,
                )

                return {
                    "success": True,
                    "deleted_count": deleted_count,
                    "days_old": days_old,
                }

        except Exception as e:
            logger.error(
                "scheduled_cleanup_executions_failed",
                error=str(e),
                exc_info=True,
            )
            return {
                "success": False,
                "error": str(e),
            }

    return asyncio.run(_cleanup())


@celery_app.task(name="app.workers.scheduled_tasks.send_daily_summary_task")
def send_daily_summary_task() -> Dict[str, Any]:
    """
    Send daily summary report to administrators

    Runs daily at 9 AM
    """

    async def _send_summary():
        logger.info("scheduled_daily_summary_started")

        try:
            async with AsyncSessionLocal() as db:
                # Get yesterday's date range
                yesterday = datetime.utcnow() - timedelta(days=1)
                start_of_day = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
                end_of_day = yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)

                # Count executions
                total_result = await db.execute(
                    select(func.count(WorkflowExecutionLog.id)).where(
                        WorkflowExecutionLog.started_at >= start_of_day,
                        WorkflowExecutionLog.started_at <= end_of_day,
                    )
                )
                total_executions = total_result.scalar()

                # Count successful
                success_result = await db.execute(
                    select(func.count(WorkflowExecutionLog.id)).where(
                        WorkflowExecutionLog.started_at >= start_of_day,
                        WorkflowExecutionLog.started_at <= end_of_day,
                        WorkflowExecutionLog.status == "completed",
                    )
                )
                successful_executions = success_result.scalar()

                # Count failed
                failed_result = await db.execute(
                    select(func.count(WorkflowExecutionLog.id)).where(
                        WorkflowExecutionLog.started_at >= start_of_day,
                        WorkflowExecutionLog.started_at <= end_of_day,
                        WorkflowExecutionLog.status == "failed",
                    )
                )
                failed_executions = failed_result.scalar()

                # Calculate average duration
                avg_duration_result = await db.execute(
                    select(func.avg(WorkflowExecutionLog.total_duration_ms)).where(
                        WorkflowExecutionLog.started_at >= start_of_day,
                        WorkflowExecutionLog.started_at <= end_of_day,
                        WorkflowExecutionLog.status == "completed",
                    )
                )
                avg_duration_ms = avg_duration_result.scalar() or 0

                summary = {
                    "date": yesterday.strftime("%Y-%m-%d"),
                    "total_executions": total_executions,
                    "successful": successful_executions,
                    "failed": failed_executions,
                    "success_rate": (
                        (successful_executions / total_executions * 100)
                        if total_executions > 0
                        else 0
                    ),
                    "avg_duration_ms": int(avg_duration_ms),
                }

                logger.info(
                    "scheduled_daily_summary_completed",
                    summary=summary,
                )

                # TODO: Send email or notification with summary
                # For now, just log it

                return {
                    "success": True,
                    "summary": summary,
                }

        except Exception as e:
            logger.error(
                "scheduled_daily_summary_failed",
                error=str(e),
                exc_info=True,
            )
            return {
                "success": False,
                "error": str(e),
            }

    return asyncio.run(_send_summary())


@celery_app.task(name="app.workers.scheduled_tasks.cleanup_old_snapshots_task")
def cleanup_old_snapshots_task(keep_versions: int = 10) -> Dict[str, Any]:
    """
    Cleanup old workflow snapshots, keeping only recent versions

    Args:
        keep_versions: Number of versions to keep per workflow
    """

    async def _cleanup():
        logger.info("scheduled_cleanup_snapshots_started", keep_versions=keep_versions)

        try:
            async with AsyncSessionLocal() as db:
                # Get all workflows
                workflows_result = await db.execute(
                    select(WorkflowExecutionSnapshot.workflow_id)
                    .distinct()
                )
                workflow_ids = [row[0] for row in workflows_result.all()]

                total_deleted = 0

                # For each workflow, keep only recent versions
                for workflow_id in workflow_ids:
                    # Get snapshots ordered by version desc
                    snapshots_result = await db.execute(
                        select(WorkflowExecutionSnapshot)
                        .where(WorkflowExecutionSnapshot.workflow_id == workflow_id)
                        .order_by(WorkflowExecutionSnapshot.version.desc())
                    )
                    snapshots = snapshots_result.scalars().all()

                    # Delete old versions beyond keep_versions
                    if len(snapshots) > keep_versions:
                        to_delete = snapshots[keep_versions:]

                        for snapshot in to_delete:
                            await db.delete(snapshot)
                            total_deleted += 1

                await db.commit()

                logger.info(
                    "scheduled_cleanup_snapshots_completed",
                    deleted_count=total_deleted,
                    workflows_processed=len(workflow_ids),
                )

                return {
                    "success": True,
                    "deleted_count": total_deleted,
                    "workflows_processed": len(workflow_ids),
                }

        except Exception as e:
            logger.error(
                "scheduled_cleanup_snapshots_failed",
                error=str(e),
                exc_info=True,
            )
            return {
                "success": False,
                "error": str(e),
            }

    return asyncio.run(_cleanup())


@celery_app.task(name="app.workers.scheduled_tasks.health_check_task")
def health_check_task() -> Dict[str, Any]:
    """
    Perform health check on the system

    Checks:
    - Database connection
    - Redis connection
    - Worker responsiveness
    """

    async def _health_check():
        logger.info("scheduled_health_check_started")

        health_status = {
            "timestamp": datetime.utcnow().isoformat(),
            "database": False,
            "redis": False,
            "workers": True,  # If this task is running, workers are responsive
        }

        try:
            # Check database
            async with AsyncSessionLocal() as db:
                await db.execute(select(1))
                health_status["database"] = True

        except Exception as e:
            logger.error("health_check_database_failed", error=str(e))

        try:
            # Check Redis (via Celery)
            from app.workers.celery_app import celery_app
            celery_app.control.ping(timeout=1.0)
            health_status["redis"] = True

        except Exception as e:
            logger.error("health_check_redis_failed", error=str(e))

        # Determine overall health
        all_healthy = all([
            health_status["database"],
            health_status["redis"],
            health_status["workers"],
        ])

        if all_healthy:
            logger.info("scheduled_health_check_completed", status="healthy")
        else:
            logger.warning("scheduled_health_check_completed", status="unhealthy", health_status=health_status)

        return {
            "success": True,
            "health_status": health_status,
            "overall_health": "healthy" if all_healthy else "unhealthy",
        }

    return asyncio.run(_health_check())
