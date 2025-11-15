"""User schemas"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base user schema"""

    email: EmailStr
    name: str = Field(min_length=1, max_length=255)


class UserCreate(UserBase):
    """User creation schema"""

    password: str = Field(min_length=8, max_length=128)


class UserUpdate(BaseModel):
    """User update schema"""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    image: Optional[str] = None


class UserRead(UserBase):
    """User read schema"""

    id: str
    email_verified: bool
    image: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class SessionRead(BaseModel):
    """Session read schema"""

    id: str
    token: str
    expires_at: datetime
    user_id: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


# Alias for backward compatibility
UserOut = UserRead
