# Architecture

This document provides an overview of the architecture of the Pankh.AI platform, including the decision-making process for key components and the final directory structure.

## 1. Socket.IO Implementation Decision

**Decision:** Integrate Socket.IO into the existing Python backend (FastAPI) rather than maintaining a separate Node.js service.

### 1.1. Context

The old architecture had a separate Socket.IO server built with Bun/Node.js TypeScript. The new backend has stub files for Socket.IO.

### 1.2. Options Considered

-   **Option A: Python Socket.IO in FastAPI (CHOSEN):** Integrate Socket.IO directly into the existing FastAPI backend using `python-socketio`.
-   **Option B: Separate Node.js Service:** Keep Socket.IO as a separate service and integrate with the backend via HTTP/Redis.
-   **Option C: Hybrid Approach:** Keep Node.js Socket.IO but tightly couple with the backend via Redis pub/sub.

### 1.3. Rationale

-   **Operational Simplicity:** A single backend service is simpler to deploy, monitor, and scale.
-   **Shared Authentication:** Reuse the existing JWT/OAuth system.
-   **Shared Database Access:** Direct access to SQLAlchemy models.
-   **`python-socketio` is Production-Ready:** The library is mature, well-maintained, and has native ASGI integration with FastAPI.
-   **One-Time Cost:** The one-time cost of rewriting the event handlers is less than the perpetual complexity of maintaining two separate services.

## 2. Directory Structure

The complete backend directory structure after the implementation of the Workers and Realtime services is as follows:

```
services/backend/
├── alembic/                          # Database migrations
│   ├── versions/                     # Migration files
│   └── env.py                        # Alembic configuration
│
├── app/                              # Main application
│   ├── api/                          # REST API endpoints
│   │   └── v1/
│   │       ├── auth.py               # Authentication endpoints
│   │       ├── billing.py            # Billing endpoints
│   │       ├── blocks.py             # Block management
│   │       ├── executions.py         # Execution endpoints
│   │       ├── tasks.py              # Task management
│   │       └── workflows.py          # Workflow CRUD
│   ├── core/                         # Core utilities
│   │   ├── auth.py                   # JWT authentication
│   │   ├── config.py                 # Settings management
│   │   ├── logging.py                # Structured logging
│   │   └── security.py               # Security utilities
│   ├── db/                           # Database
│   │   ├── base.py                   # Base model
│   │   ├── session.py                # Database session
│   │   └── models/                   # SQLAlchemy models
│   ├── executor/                     # Workflow execution engine
│   │   ├── engine.py                 # LangGraph executor
│   │   ├── state.py                  # Execution state
│   │   ├── variable_resolver.py      # Variable resolution
│   │   └── blocks/                   # Workflow blocks
│   ├── realtime/                     # Socket.IO service
│   │   ├── socketio_app.py           # Socket.IO server
│   │   ├── rooms.py                  # Room management
│   │   ├── notifications.py          # Notification manager
│   │   ├── events.py                 # Event handlers
│   │   └── execution_notifier.py     # Execution integration
│   ├── schemas/                      # Pydantic schemas
│   ├── services/                     # Business logic services
│   │   └── ai/                       # AI services
│   ├── workers/                      # Celery workers
│   │   ├── celery_app.py             # Celery config
│   │   ├── tasks.py                  # Main tasks
│   │   └── scheduled_tasks.py        # Scheduled tasks
│   └── main.py                       # FastAPI app
├── scripts/                          # Startup scripts
├── tests/                            # Test suite
├── .env                              # Environment variables
├── .env.example                      # Environment template
├── alembic.ini                       # Alembic configuration
├── check_env.py                      # Environment checker
├── Dockerfile                        # Docker image
├── pyproject.toml                    # Python dependencies
└── README.md                         # Project README
```

## Additional Architecture Content

### Migration Plan

Content from `MIGRATION_PLAN.md`.

### Migration Status Update

Content from `MIGRATION_STATUS_UPDATE.md`.
