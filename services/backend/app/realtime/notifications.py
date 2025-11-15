"""Notification Manager for Real-time Events"""

from typing import Any, Dict, List, Optional
from datetime import datetime
from enum import Enum

from app.core.logging import get_logger
from .rooms import room_manager

logger = get_logger(__name__)


class NotificationType(str, Enum):
    """Notification types"""

    # Workflow events
    WORKFLOW_CREATED = "workflow.created"
    WORKFLOW_UPDATED = "workflow.updated"
    WORKFLOW_DELETED = "workflow.deleted"
    WORKFLOW_DEPLOYED = "workflow.deployed"

    # Execution events
    EXECUTION_STARTED = "execution.started"
    EXECUTION_PROGRESS = "execution.progress"
    EXECUTION_COMPLETED = "execution.completed"
    EXECUTION_FAILED = "execution.failed"
    EXECUTION_CANCELLED = "execution.cancelled"

    # Block events
    BLOCK_STARTED = "block.started"
    BLOCK_COMPLETED = "block.completed"
    BLOCK_FAILED = "block.failed"

    # Collaboration events
    USER_JOINED = "user.joined"
    USER_LEFT = "user.left"
    CURSOR_MOVED = "cursor.moved"
    SELECTION_CHANGED = "selection.changed"

    # System events
    SYSTEM_NOTIFICATION = "system.notification"
    TASK_QUEUED = "task.queued"
    TASK_COMPLETED = "task.completed"


class NotificationManager:
    """Manages real-time notifications via Socket.IO"""

    def __init__(self, sio):
        """Initialize notification manager

        Args:
            sio: Socket.IO server instance
        """
        self.sio = sio

    async def emit_to_room(
        self,
        room_id: str,
        event: str,
        data: Dict[str, Any],
        skip_sid: Optional[str] = None,
    ):
        """Emit event to all sockets in a room

        Args:
            room_id: Room to emit to
            event: Event name
            data: Event data
            skip_sid: Optional socket ID to skip
        """
        try:
            await self.sio.emit(
                event,
                data,
                room=room_id,
                skip_sid=skip_sid,
            )

            logger.debug(
                "notification_emitted",
                room_id=room_id,
                event=event,
                skip_sid=skip_sid,
            )

        except Exception as e:
            logger.error(
                "notification_emit_failed",
                room_id=room_id,
                event=event,
                error=str(e),
                exc_info=True,
            )

    async def emit_to_user(
        self,
        user_id: str,
        event: str,
        data: Dict[str, Any],
    ):
        """Emit event to a specific user

        Args:
            user_id: User identifier
            event: Event name
            data: Event data
        """
        room_id = room_manager.get_user_room_id(user_id)
        await self.emit_to_room(room_id, event, data)

    async def notify_workflow_event(
        self,
        workflow_id: str,
        event_type: NotificationType,
        data: Dict[str, Any],
        skip_sid: Optional[str] = None,
    ):
        """Notify workflow-related event

        Args:
            workflow_id: Workflow identifier
            event_type: Type of notification
            data: Event data
            skip_sid: Optional socket ID to skip
        """
        room_id = room_manager.get_workflow_room_id(workflow_id)

        notification = {
            "type": event_type.value,
            "workflow_id": workflow_id,
            "timestamp": datetime.utcnow().isoformat(),
            "data": data,
        }

        await self.emit_to_room(
            room_id=room_id,
            event="workflow_event",
            data=notification,
            skip_sid=skip_sid,
        )

    async def notify_execution_started(
        self,
        execution_id: str,
        workflow_id: str,
        user_id: str,
        input_data: Dict[str, Any],
    ):
        """Notify execution started

        Args:
            execution_id: Execution identifier
            workflow_id: Workflow identifier
            user_id: User who started execution
            input_data: Execution input data
        """
        # Notify workflow room
        workflow_room = room_manager.get_workflow_room_id(workflow_id)
        await self.emit_to_room(
            room_id=workflow_room,
            event="execution_started",
            data={
                "type": NotificationType.EXECUTION_STARTED.value,
                "execution_id": execution_id,
                "workflow_id": workflow_id,
                "user_id": user_id,
                "input": input_data,
                "timestamp": datetime.utcnow().isoformat(),
            },
        )

        # Notify user
        await self.emit_to_user(
            user_id=user_id,
            event="execution_started",
            data={
                "execution_id": execution_id,
                "workflow_id": workflow_id,
            },
        )

        logger.info(
            "execution_started_notified",
            execution_id=execution_id,
            workflow_id=workflow_id,
        )

    async def notify_execution_progress(
        self,
        execution_id: str,
        workflow_id: str,
        block_id: str,
        block_type: str,
        status: str,
        output: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
    ):
        """Notify execution progress (block completed)

        Args:
            execution_id: Execution identifier
            workflow_id: Workflow identifier
            block_id: Current block identifier
            block_type: Block type
            status: Block status (started, completed, failed)
            output: Block output data
            error: Error message if failed
        """
        execution_room = room_manager.get_execution_room_id(execution_id)

        notification = {
            "type": NotificationType.EXECUTION_PROGRESS.value,
            "execution_id": execution_id,
            "workflow_id": workflow_id,
            "block_id": block_id,
            "block_type": block_type,
            "status": status,
            "timestamp": datetime.utcnow().isoformat(),
        }

        if output:
            notification["output"] = output
        if error:
            notification["error"] = error

        await self.emit_to_room(
            room_id=execution_room,
            event="execution_progress",
            data=notification,
        )

        logger.debug(
            "execution_progress_notified",
            execution_id=execution_id,
            block_id=block_id,
            status=status,
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
        """Notify execution completed

        Args:
            execution_id: Execution identifier
            workflow_id: Workflow identifier
            user_id: User who started execution
            success: Whether execution succeeded
            output: Final output data
            error: Error message if failed
            duration_ms: Execution duration in milliseconds
        """
        event_type = (
            NotificationType.EXECUTION_COMPLETED
            if success
            else NotificationType.EXECUTION_FAILED
        )

        notification = {
            "type": event_type.value,
            "execution_id": execution_id,
            "workflow_id": workflow_id,
            "success": success,
            "timestamp": datetime.utcnow().isoformat(),
        }

        if output:
            notification["output"] = output
        if error:
            notification["error"] = error
        if duration_ms:
            notification["duration_ms"] = duration_ms

        # Notify execution room
        execution_room = room_manager.get_execution_room_id(execution_id)
        await self.emit_to_room(
            room_id=execution_room,
            event="execution_completed",
            data=notification,
        )

        # Notify workflow room
        workflow_room = room_manager.get_workflow_room_id(workflow_id)
        await self.emit_to_room(
            room_id=workflow_room,
            event="execution_completed",
            data=notification,
        )

        # Notify user
        await self.emit_to_user(
            user_id=user_id,
            event="execution_completed",
            data=notification,
        )

        logger.info(
            "execution_completed_notified",
            execution_id=execution_id,
            workflow_id=workflow_id,
            success=success,
        )

    async def notify_collaboration_event(
        self,
        workflow_id: str,
        user_id: str,
        event_type: NotificationType,
        data: Dict[str, Any],
        skip_sid: Optional[str] = None,
    ):
        """Notify collaboration event (cursor, selection, etc.)

        Args:
            workflow_id: Workflow being edited
            user_id: User performing action
            event_type: Type of collaboration event
            data: Event data
            skip_sid: Socket ID to skip (usually sender)
        """
        room_id = room_manager.get_workflow_room_id(workflow_id)

        notification = {
            "type": event_type.value,
            "workflow_id": workflow_id,
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat(),
            "data": data,
        }

        await self.emit_to_room(
            room_id=room_id,
            event="collaboration_event",
            data=notification,
            skip_sid=skip_sid,
        )

    async def notify_system_event(
        self,
        organization_id: str,
        event_type: NotificationType,
        message: str,
        data: Optional[Dict[str, Any]] = None,
    ):
        """Notify system-wide event

        Args:
            organization_id: Organization identifier
            event_type: Type of system event
            message: Human-readable message
            data: Additional event data
        """
        room_id = room_manager.get_organization_room_id(organization_id)

        notification = {
            "type": event_type.value,
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
        }

        if data:
            notification["data"] = data

        await self.emit_to_room(
            room_id=room_id,
            event="system_notification",
            data=notification,
        )

    async def broadcast_to_all(
        self,
        event: str,
        data: Dict[str, Any],
    ):
        """Broadcast event to all connected clients

        Args:
            event: Event name
            data: Event data
        """
        try:
            await self.sio.emit(event, data)

            logger.info(
                "broadcast_sent",
                event=event,
            )

        except Exception as e:
            logger.error(
                "broadcast_failed",
                event=event,
                error=str(e),
                exc_info=True,
            )
