"""Pankh.AI Backend - Main FastAPI Application"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1 import api_router
from app.core.config import settings
from app.core.logging import get_logger, set_trace_id, setup_logging
from app.db.session import engine
from app.realtime import get_socketio_app

# Set up logging
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan events"""
    # Startup
    logger.info("starting_application", version=settings.VERSION)

    # TODO: Initialize database connection pool
    # TODO: Initialize Redis connection
    # TODO: Start background tasks

    yield

    # Shutdown
    logger.info("shutting_down_application")
    await engine.dispose()


# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS middleware - temporarily allow all for development
logger.info("configuring_cors", origins=["*"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request ID middleware
@app.middleware("http")
async def add_trace_id_middleware(request, call_next):
    """Add trace ID to each request"""
    import uuid

    trace_id = request.headers.get("X-Trace-ID", str(uuid.uuid4()))
    set_trace_id(trace_id)

    response = await call_next(request)
    response.headers["X-Trace-ID"] = trace_id
    return response


# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return JSONResponse(
        content={
            "status": "healthy",
            "version": settings.VERSION,
            "service": "pankh-ai-backend",
        }
    )


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Pankh.AI Backend API",
        "version": settings.VERSION,
        "docs": "/docs",
        "health": "/health",
    }


# Mount Socket.IO app at /socket.io
socketio_app = get_socketio_app()
app.mount("/socket.io", socketio_app)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        workers=settings.WORKERS if not settings.RELOAD else 1,
        log_level=settings.LOG_LEVEL.lower(),
    )
