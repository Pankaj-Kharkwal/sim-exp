"""API v1 router"""

from fastapi import APIRouter

from app.api.v1 import (
    auth,
    billing,
    blocks,
    ai_blocks,
    chat,
    copilot,
    executions,
    tasks,
    workflows,
    knowledge,
    files,
    organizations,
    folders,
    templates,
)

api_router = APIRouter()

# Include sub-routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(workflows.router, prefix="/workflows", tags=["Workflows"])
api_router.include_router(blocks.router)  # Already has prefix and tags
api_router.include_router(ai_blocks.router)  # Already has prefix and tags
api_router.include_router(executions.router, prefix="/executions", tags=["Executions"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
api_router.include_router(chat.router)  # Already has prefix and tags
api_router.include_router(copilot.router)  # Already has prefix and tags
api_router.include_router(billing.router, prefix="/billing", tags=["Billing"])
api_router.include_router(knowledge.router, prefix="/knowledge", tags=["Knowledge Base"])
api_router.include_router(files.router, prefix="/files", tags=["Files & Storage"])
api_router.include_router(organizations.router, prefix="/organizations", tags=["Organizations & Workspaces"])
api_router.include_router(folders.router, prefix="/folders", tags=["Folders"])
api_router.include_router(templates.router, prefix="/templates", tags=["Templates"])
