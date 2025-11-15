"""Create dummy users for development/testing"""

import asyncio
import sys
import uuid
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.db.models.user import User, Account
from app.core.security import get_password_hash


async def create_dummy_users():
    """Create dummy users for testing"""

    dummy_users = [
        {
            "email": "admin@pankh.ai",
            "password": "admin123",
            "name": "Admin User",
        },
        {
            "email": "user@pankh.ai",
            "password": "user123",
            "name": "Test User",
        },
        {
            "email": "demo@pankh.ai",
            "password": "demo123",
            "name": "Demo User",
        },
    ]

    async with AsyncSessionLocal() as db:
        for user_data in dummy_users:
            # Check if user already exists
            result = await db.execute(
                select(User).where(User.email == user_data["email"])
            )
            existing_user = result.scalar_one_or_none()

            if existing_user:
                print(f"✓ User {user_data['email']} already exists")
                continue

            # Create new user
            user_id = str(uuid.uuid4())
            user = User(
                id=user_id,
                email=user_data["email"],
                name=user_data["name"],
                email_verified=True,
            )

            db.add(user)

            # Create credentials account (password-based)
            account = Account(
                id=str(uuid.uuid4()),
                user_id=user_id,
                account_id=user_data["email"],
                provider_id="credentials",  # Password-based provider
                password=get_password_hash(user_data["password"]),
            )

            db.add(account)
            await db.commit()

            print(f"✓ Created user: {user_data['email']} (password: {user_data['password']})")

    print("\n" + "="*60)
    print("Dummy users created successfully!")
    print("="*60)
    print("\nLogin credentials:")
    print("-" * 60)
    for user_data in dummy_users:
        print(f"  Email:    {user_data['email']}")
        print(f"  Password: {user_data['password']}")
        print("-" * 60)


if __name__ == "__main__":
    print("Creating dummy users...")
    asyncio.run(create_dummy_users())
