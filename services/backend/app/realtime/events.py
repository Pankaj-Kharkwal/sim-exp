"""Socket.IO Event Handlers"""

from typing import Dict, Any, Optional
import socketio

from app.core.logging import get_logger
from app.core.auth import verify_token
from .rooms import room_manager
from .notifications import NotificationManager

logger = get_logger(__name__)


def register_event_handlers(sio: socketio.AsyncServer):
    """Register all Socket.IO event handlers

    Args:
        sio: Socket.IO server instance
    """
    notification_manager = NotificationManager(sio)

    @sio.event
    async def connect(sid: str, environ: Dict, auth: Optional[Dict] = None):
        """Handle client connection

        Args:
            sid: Socket session ID
            environ: ASGI environ dict
            auth: Authentication data
        """
        try:
            # Verify authentication
            if not auth or "token" not in auth:
                logger.warning("connection_rejected_no_token", sid=sid)
                return False

            token = auth["token"]

            # Verify JWT token
            try:
                payload = verify_token(token)
                user_id = payload.get("sub")

                if not user_id:
                    logger.warning("connection_rejected_invalid_token", sid=sid)
                    return False

                # Store user info in session
                await sio.save_session(
                    sid,
                    {
                        "user_id": user_id,
                        "authenticated": True,
                    },
                )

                # Auto-join user's personal room
                user_room_id = room_manager.get_user_room_id(user_id)
                room_manager.create_room(user_room_id, "user", {"user_id": user_id})
                room_manager.join_room(sid, user_room_id)
                await sio.enter_room(sid, user_room_id)

                logger.info(
                    "client_connected",
                    sid=sid,
                    user_id=user_id,
                )

                return True

            except Exception as e:
                logger.error(
                    "auth_verification_failed",
                    sid=sid,
                    error=str(e),
                    exc_info=True,
                )
                return False

        except Exception as e:
            logger.error(
                "connection_error",
                sid=sid,
                error=str(e),
                exc_info=True,
            )
            return False

    @sio.event
    async def disconnect(sid: str):
        """Handle client disconnection

        Args:
            sid: Socket session ID
        """
        try:
            session = await sio.get_session(sid)
            user_id = session.get("user_id")

            # Leave all rooms
            room_manager.disconnect_socket(sid)

            logger.info(
                "client_disconnected",
                sid=sid,
                user_id=user_id,
            )

        except Exception as e:
            logger.error(
                "disconnect_error",
                sid=sid,
                error=str(e),
                exc_info=True,
            )

    @sio.event
    async def join_workflow(sid: str, data: Dict[str, Any]):
        """Join a workflow room for real-time updates

        Args:
            sid: Socket session ID
            data: {"workflow_id": str}
        """
        try:
            session = await sio.get_session(sid)
            user_id = session.get("user_id")

            if not user_id:
                await sio.emit("error", {"message": "Not authenticated"}, to=sid)
                return

            workflow_id = data.get("workflow_id")
            if not workflow_id:
                await sio.emit("error", {"message": "workflow_id required"}, to=sid)
                return

            # Create and join workflow room
            room_id = room_manager.get_workflow_room_id(workflow_id)
            room_manager.create_room(room_id, "workflow", {"workflow_id": workflow_id})
            room_manager.join_room(sid, room_id)
            await sio.enter_room(sid, room_id)

            # Notify others in room
            await notification_manager.emit_to_room(
                room_id=room_id,
                event="user_joined_workflow",
                data={
                    "user_id": user_id,
                    "workflow_id": workflow_id,
                },
                skip_sid=sid,
            )

            # Confirm join
            await sio.emit(
                "workflow_joined",
                {"workflow_id": workflow_id, "room_id": room_id},
                to=sid,
            )

            logger.info(
                "user_joined_workflow",
                sid=sid,
                user_id=user_id,
                workflow_id=workflow_id,
            )

        except Exception as e:
            logger.error(
                "join_workflow_error",
                sid=sid,
                error=str(e),
                exc_info=True,
            )
            await sio.emit("error", {"message": str(e)}, to=sid)

    @sio.event
    async def leave_workflow(sid: str, data: Dict[str, Any]):
        """Leave a workflow room

        Args:
            sid: Socket session ID
            data: {"workflow_id": str}
        """
        try:
            session = await sio.get_session(sid)
            user_id = session.get("user_id")

            workflow_id = data.get("workflow_id")
            if not workflow_id:
                return

            # Leave workflow room
            room_id = room_manager.get_workflow_room_id(workflow_id)
            room_manager.leave_room(sid, room_id)
            await sio.leave_room(sid, room_id)

            # Notify others
            await notification_manager.emit_to_room(
                room_id=room_id,
                event="user_left_workflow",
                data={
                    "user_id": user_id,
                    "workflow_id": workflow_id,
                },
            )

            logger.info(
                "user_left_workflow",
                sid=sid,
                user_id=user_id,
                workflow_id=workflow_id,
            )

        except Exception as e:
            logger.error(
                "leave_workflow_error",
                sid=sid,
                error=str(e),
                exc_info=True,
            )

    @sio.event
    async def join_execution(sid: str, data: Dict[str, Any]):
        """Join an execution room for real-time progress updates

        Args:
            sid: Socket session ID
            data: {"execution_id": str}
        """
        try:
            session = await sio.get_session(sid)
            user_id = session.get("user_id")

            if not user_id:
                await sio.emit("error", {"message": "Not authenticated"}, to=sid)
                return

            execution_id = data.get("execution_id")
            if not execution_id:
                await sio.emit("error", {"message": "execution_id required"}, to=sid)
                return

            # Create and join execution room
            room_id = room_manager.get_execution_room_id(execution_id)
            room_manager.create_room(room_id, "execution", {"execution_id": execution_id})
            room_manager.join_room(sid, room_id)
            await sio.enter_room(sid, room_id)

            # Confirm join
            await sio.emit(
                "execution_joined",
                {"execution_id": execution_id, "room_id": room_id},
                to=sid,
            )

            logger.info(
                "user_joined_execution",
                sid=sid,
                user_id=user_id,
                execution_id=execution_id,
            )

        except Exception as e:
            logger.error(
                "join_execution_error",
                sid=sid,
                error=str(e),
                exc_info=True,
            )
            await sio.emit("error", {"message": str(e)}, to=sid)

    @sio.event
    async def leave_execution(sid: str, data: Dict[str, Any]):
        """Leave an execution room

        Args:
            sid: Socket session ID
            data: {"execution_id": str}
        """
        try:
            execution_id = data.get("execution_id")
            if not execution_id:
                return

            # Leave execution room
            room_id = room_manager.get_execution_room_id(execution_id)
            room_manager.leave_room(sid, room_id)
            await sio.leave_room(sid, room_id)

            logger.info(
                "user_left_execution",
                sid=sid,
                execution_id=execution_id,
            )

        except Exception as e:
            logger.error(
                "leave_execution_error",
                sid=sid,
                error=str(e),
                exc_info=True,
            )

    @sio.event
    async def cursor_move(sid: str, data: Dict[str, Any]):
        """Handle cursor movement in collaborative editing

        Args:
            sid: Socket session ID
            data: {"workflow_id": str, "position": {"x": int, "y": int}}
        """
        try:
            session = await sio.get_session(sid)
            user_id = session.get("user_id")

            workflow_id = data.get("workflow_id")
            position = data.get("position")

            if not workflow_id or not position:
                return

            # Broadcast to workflow room (except sender)
            room_id = room_manager.get_workflow_room_id(workflow_id)
            await notification_manager.emit_to_room(
                room_id=room_id,
                event="cursor_moved",
                data={
                    "user_id": user_id,
                    "position": position,
                },
                skip_sid=sid,
            )

        except Exception as e:
            logger.error(
                "cursor_move_error",
                sid=sid,
                error=str(e),
                exc_info=True,
            )

    @sio.event
    async def selection_change(sid: str, data: Dict[str, Any]):
        """Handle selection change in collaborative editing

        Args:
            sid: Socket session ID
            data: {"workflow_id": str, "block_ids": List[str]}
        """
        try:
            session = await sio.get_session(sid)
            user_id = session.get("user_id")

            workflow_id = data.get("workflow_id")
            block_ids = data.get("block_ids", [])

            if not workflow_id:
                return

            # Broadcast to workflow room (except sender)
            room_id = room_manager.get_workflow_room_id(workflow_id)
            await notification_manager.emit_to_room(
                room_id=room_id,
                event="selection_changed",
                data={
                    "user_id": user_id,
                    "block_ids": block_ids,
                },
                skip_sid=sid,
            )

        except Exception as e:
            logger.error(
                "selection_change_error",
                sid=sid,
                error=str(e),
                exc_info=True,
            )

    @sio.event
    async def block_update(sid: str, data: Dict[str, Any]):
        """Handle block update in workflow

        Args:
            sid: Socket session ID
            data: {"workflow_id": str, "block": {...}}
        """
        try:
            session = await sio.get_session(sid)
            user_id = session.get("user_id")

            workflow_id = data.get("workflow_id")
            block = data.get("block")

            if not workflow_id or not block:
                return

            # Broadcast to workflow room (except sender)
            room_id = room_manager.get_workflow_room_id(workflow_id)
            await notification_manager.emit_to_room(
                room_id=room_id,
                event="block_updated",
                data={
                    "user_id": user_id,
                    "workflow_id": workflow_id,
                    "block": block,
                },
                skip_sid=sid,
            )

            logger.debug("block_update_broadcast", workflow_id=workflow_id, block_id=block.get("id"))

        except Exception as e:
            logger.error(
                "block_update_error",
                sid=sid,
                error=str(e),
                exc_info=True,
            )

    @sio.event
    async def workflow_state_change(sid: str, data: Dict[str, Any]):
        """Handle workflow state change (blocks/edges added/removed)

        Args:
            sid: Socket session ID
            data: {"workflow_id": str, "changes": {...}}
        """
        try:
            session = await sio.get_session(sid)
            user_id = session.get("user_id")

            workflow_id = data.get("workflow_id")
            changes = data.get("changes")

            if not workflow_id or not changes:
                return

            # Broadcast to workflow room (except sender)
            room_id = room_manager.get_workflow_room_id(workflow_id)
            await notification_manager.emit_to_room(
                room_id=room_id,
                event="workflow_state_changed",
                data={
                    "user_id": user_id,
                    "workflow_id": workflow_id,
                    "changes": changes,
                },
                skip_sid=sid,
            )

            logger.debug("workflow_state_change_broadcast", workflow_id=workflow_id)

        except Exception as e:
            logger.error(
                "workflow_state_change_error",
                sid=sid,
                error=str(e),
                exc_info=True,
            )

    @sio.event
    async def ping(sid: str):
        """Handle ping from client

        Args:
            sid: Socket session ID
        """
        await sio.emit("pong", to=sid)

    logger.info("socketio_event_handlers_registered")
