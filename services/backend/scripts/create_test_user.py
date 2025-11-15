#!/usr/bin/env python3
"""Create a test user for development and testing"""

import asyncio
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.db.models.user import User, Account
from app.core.security import get_password_hash


async def create_test_user():
    """Create a test user for development"""
    async with AsyncSessionLocal() as session:
        # Check if user already exists
        result = await session.execute(select(User).where(User.email == "test@pankh.ai"))
        existing_user = result.scalar_one_or_none()

        if existing_user:
            print(f"✅ Test user already exists: {existing_user.email}")
            return

        now = datetime.now(timezone.utc)

        # Create user
        user = User(
            id=str(uuid.uuid4()),
            email="test@pankh.ai",
            name="Test User",
            email_verified=True,
            created_at=now,
            updated_at=now,
        )
        session.add(user)
        await session.flush()  # Get user.id

        # Create credentials account
        hashed_password = get_password_hash("Test123!")
        account = Account(
            id=str(uuid.uuid4()),
            user_id=user.id,
            provider_id="credentials",
            account_id=user.email,
            password=hashed_password,
            created_at=now,
            updated_at=now,
        )
        session.add(account)

        await session.commit()

        print(
            """
✅ Test user created successfully!

Credentials:
  Email:    test@pankh.ai
  Password: Test123!

You can now login using these credentials.
"""
        )


async def main():
    """Main function"""
    try:
        print("Creating test user...")
        await create_test_user()
    except Exception as e:
        print(f"❌ Error creating test user: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
