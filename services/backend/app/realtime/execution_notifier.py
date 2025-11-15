"""Execution Event Notifier for Real-time Updates

Integrates with workflow executor to emit real-time events
"""

from typing import Any, Dict, Optional
from datetime import datetime

from app.core.logging import get_logger
from .socketio_app import sio
from .notifications import NotificationManager

logger = get_logger(__name__)


class ExecutionNotifier:
    """Emits real-time events during workflow execution"""

    def __init__(self):
        self.notification_manager = NotificationManager(sio)

    async def notify_execution_started(
        self,
        execution_id: str,
        workflow_id: str,
        user_id: str,
        input_data: Dict[str, Any],
    ):
        """Notify that execution has started

        Args:
            execution_id: Execution identifier
            workflow_id: Workflow identifier
            user_id: User who started execution
            input_data: Input data for execution
        """
        try:
            await self.notification_manager.notify_execution_started(
                execution_id=execution_id,
                workflow_id=workflow_id,
                user_id=user_id,
                input_data=input_data,
            )
        except Exception as e:
            logger.error(
                "failed_to_notify_execution_started",
                execution_id=execution_id,
                error=str(e),
                exc_info=True,
            )

    async def notify_block_started(
        self,
        execution_id: str,
        workflow_id: str,
        block_id: str,
        block_type: str,
    ):
        """Notify that a block has started executing

        Args:
            execution_id: Execution identifier
            workflow_id: Workflow identifier
            block_id: Block identifier
            block_type: Type of block
        """
        try:
            await self.notification_manager.notify_execution_progress(
                execution_id=execution_id,
                workflow_id=workflow_id,
                block_id=block_id,
                block_type=block_type,
                status="started",
            )
        except Exception as e:
            logger.error(
                "failed_to_notify_block_started",
                execution_id=execution_id,
                block_id=block_id,
                error=str(e),
                exc_info=True,
            )

    async def notify_block_completed(
        self,
        execution_id: str,
        workflow_id: str,
        block_id: str,
        block_type: str,
        output: Optional[Dict[str, Any]] = None,
    ):
        """Notify that a block has completed successfully

        Args:
            execution_id: Execution identifier
            workflow_id: Workflow identifier
            block_id: Block identifier
            block_type: Type of block
            output: Block output data
        """
        try:
            await self.notification_manager.notify_execution_progress(
                execution_id=execution_id,
                workflow_id=workflow_id,
                block_id=block_id,
                block_type=block_type,
                status="completed",
                output=output,
            )
        except Exception as e:
            logger.error(
                "failed_to_notify_block_completed",
                execution_id=execution_id,
                block_id=block_id,
                error=str(e),
                exc_info=True,
            )

    async def notify_block_failed(
        self,
        execution_id: str,
        workflow_id: str,
        block_id: str,
        block_type: str,
        error: str,
    ):
        """Notify that a block has failed

        Args:
            execution_id: Execution identifier
            workflow_id: Workflow identifier
            block_id: Block identifier
            block_type: Type of block
            error: Error message
        """
        try:
            await self.notification_manager.notify_execution_progress(
                execution_id=execution_id,
                workflow_id=workflow_id,
                block_id=block_id,
                block_type=block_type,
                status="failed",
                error=error,
            )
        except Exception as e:
            logger.error(
                "failed_to_notify_block_failed",
                execution_id=execution_id,
                block_id=block_id,
                error=str(e),
                exc_info=True,
            )

    async def notify_execution_completed(
        self,
        execution_id: str,
        workflow_id: str,
        user_id: str,
        success: bool,
        output: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
        duration_ms: Optional[int] = None,
    ):
        """Notify that execution has completed

        Args:
            execution_id: Execution identifier
            workflow_id: Workflow identifier
            user_id: User who started execution
            success: Whether execution succeeded
            output: Final output data
            error: Error message if failed
            duration_ms: Execution duration in milliseconds
        """
        try:
            await self.notification_manager.notify_execution_completed(
                execution_id=execution_id,
                workflow_id=workflow_id,
                user_id=user_id,
                success=success,
                output=output,
                error=error,
                duration_ms=duration_ms,
            )
        except Exception as e:
            logger.error(
                "failed_to_notify_execution_completed",
                execution_id=execution_id,
                error=str(e),
                exc_info=True,
            )


# Global execution notifier instance
execution_notifier = ExecutionNotifier()
