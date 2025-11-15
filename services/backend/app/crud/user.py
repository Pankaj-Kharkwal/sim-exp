"""User CRUD operations"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.user import User
from app.schemas.user import UserCreate


async def get_user(db: AsyncSession, user_id: str) -> User | None:
    """
    Get a user by ID.
    """
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """
    Get a user by email.
    """
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def create_user(
    db: AsyncSession, user: UserCreate, hashed_password: str
) -> User:
    """
    Create a new user.
    """
    from uuid import uuid4
    from app.db.models.user import Account

    # Create user
    from datetime import datetime, timezone
    user_id = str(uuid4())
    now = datetime.now(timezone.utc)
    db_user = User(
        id=user_id,
        email=user.email,
        name=user.name,
        created_at=now,
        updated_at=now,
    )
    db.add(db_user)

    # Create credentials account with hashed password
    account_id = str(uuid4())
    db_account = Account(
        id=account_id,
        account_id=user.email,
        provider_id="credentials",
        password=hashed_password,
        user_id=user_id,
        created_at=now,
        updated_at=now,
    )
    db.add(db_account)

    await db.commit()
    await db.refresh(db_user)
    return db_user
