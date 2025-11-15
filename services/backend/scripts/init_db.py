"""
Database Initialization Script

Run this script to create all database tables and initial data.

Usage:
    python scripts/init_db.py
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings
from app.core.logging import get_logger, setup_logging
from app.db.base import Base

# Import all models to register them with Base
from app.db.models import (
    User,
    Session,
    Account,
    Verification,
    Organization,
    OrganizationMember,
    Workspace,
    Workflow,
    WorkflowBlock,
    WorkflowEdge,
    WorkflowFolder,
    WorkflowSubflow,
    WorkflowExecutionSnapshot,
    WorkflowExecutionLog,
    APIKey,
    KnowledgeBase,
    Document,
    DocumentChunk,
    TagDefinition,
    Folder,
)

setup_logging()
logger = get_logger(__name__)


async def init_database():
    """Initialize database - create all tables"""
    logger.info("database_initialization_started")

    try:
        # Create async engine
        engine = create_async_engine(
            settings.DATABASE_URL,
            echo=True,
        )

        # Create all tables
        async with engine.begin() as conn:
            logger.info("creating_database_tables")
            await conn.run_sync(Base.metadata.create_all)

        logger.info("database_tables_created_successfully")

        # Dispose engine
        await engine.dispose()

        logger.info("database_initialization_completed")
        return True

    except Exception as e:
        logger.error("database_initialization_failed", error=str(e), exc_info=True)
        return False


async def drop_database():
    """Drop all database tables - USE WITH CAUTION"""
    logger.warning("database_drop_started")

    try:
        # Create async engine
        engine = create_async_engine(
            settings.DATABASE_URL,
            echo=True,
        )

        # Drop all tables
        async with engine.begin() as conn:
            logger.warning("dropping_database_tables")
            await conn.run_sync(Base.metadata.drop_all)

        logger.warning("database_tables_dropped")

        # Dispose engine
        await engine.dispose()

        logger.info("database_drop_completed")
        return True

    except Exception as e:
        logger.error("database_drop_failed", error=str(e), exc_info=True)
        return False


async def create_demo_data():
    """Create demo data for testing"""
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import sessionmaker
    import uuid
    from datetime import datetime

    logger.info("creating_demo_data")

    try:
        engine = create_async_engine(settings.DATABASE_URL)
        AsyncSessionLocal = sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

        async with AsyncSessionLocal() as db:
            # Create demo organization
            org = Organization(
                id=str(uuid.uuid4()),
                name="Demo Organization",
                slug="demo-org",
                description="Demo organization for testing",
            )
            db.add(org)

            # Create demo user
            user = User(
                id=str(uuid.uuid4()),
                name="Demo User",
                email="demo@pankh.ai",
                email_verified=True,
            )
            db.add(user)

            await db.flush()

            # Create organization membership
            member = OrganizationMember(
                id=str(uuid.uuid4()),
                organization_id=org.id,
                user_id=user.id,
                role="owner",
            )
            db.add(member)

            # Create demo workspace
            workspace = Workspace(
                id=str(uuid.uuid4()),
                name="Demo Workspace",
                description="Default workspace for testing",
                organization_id=org.id,
                owner_id=user.id,
                is_default=True,
            )
            db.add(workspace)

            await db.flush()

            # Create demo workflow
            workflow = Workflow(
                id=str(uuid.uuid4()),
                name="Demo Workflow",
                description="A sample workflow for testing",
                user_id=user.id,
                workspace_id=workspace.id,
                last_synced=datetime.utcnow(),
            )
            db.add(workflow)

            await db.commit()

            logger.info(
                "demo_data_created",
                user_id=user.id,
                org_id=org.id,
                workspace_id=workspace.id,
                workflow_id=workflow.id,
            )

        await engine.dispose()
        return True

    except Exception as e:
        logger.error("demo_data_creation_failed", error=str(e), exc_info=True)
        return False


async def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(description="Database initialization script")
    parser.add_argument(
        "--drop",
        action="store_true",
        help="Drop all tables before creating (WARNING: destroys all data)",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Create demo data after initialization",
    )

    args = parser.parse_args()

    # Drop tables if requested
    if args.drop:
        confirm = input("⚠️  This will DELETE ALL DATA. Type 'yes' to confirm: ")
        if confirm.lower() == "yes":
            success = await drop_database()
            if not success:
                logger.error("database_drop_failed")
                sys.exit(1)
        else:
            logger.info("database_drop_cancelled")
            sys.exit(0)

    # Create tables
    success = await init_database()
    if not success:
        logger.error("database_initialization_failed")
        sys.exit(1)

    # Create demo data if requested
    if args.demo:
        success = await create_demo_data()
        if not success:
            logger.error("demo_data_creation_failed")
            sys.exit(1)

    logger.info("✅ Database setup completed successfully!")
    print("\n✅ Database initialized successfully!")

    if args.demo:
        print("\n📊 Demo data created:")
        print("   Email: demo@pankh.ai")
        print("   Organization: Demo Organization")
        print("   Workspace: Demo Workspace")
        print("   Workflow: Demo Workflow")


if __name__ == "__main__":
    asyncio.run(main())
