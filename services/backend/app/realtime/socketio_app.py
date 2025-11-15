"""Socket.IO Application Configuration"""

import socketio
from typing import Optional

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

# Create Socket.IO server with async mode
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*" if settings.ENVIRONMENT == "development" else [
        settings.FRONTEND_URL,
    ],
    logger=True,
    engineio_logger=True,
    ping_timeout=60,
    ping_interval=25,
)


def get_socketio_app():
    """Get Socket.IO ASGI application

    Returns:
        socketio.ASGIApp: Socket.IO ASGI application
    """
    from .events import register_event_handlers

    # Register all event handlers
    register_event_handlers(sio)

    logger.info(
        "socketio_app_initialized",
        cors_origins="*" if settings.ENVIRONMENT == "development" else settings.FRONTEND_URL,
    )

    return socketio.ASGIApp(sio)
