"""Folder Database Models"""

from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, String, Text, Integer
from sqlalchemy.orm import relationship
import uuid

from app.db.base import Base


class Folder(Base):
    """Folder for organizing workflows"""

    __tablename__ = "folders"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    # Hierarchy
    parent_id = Column(String, ForeignKey("folders.id"), nullable=True)
    path = Column(String(1000), nullable=False)  # Full path like "/folder1/folder2"
    level = Column(Integer, default=0)  # Depth level

    # Ownership
    user_id = Column(String, ForeignKey("user.id"), nullable=False)
    organization_id = Column(String, ForeignKey("organization.id"), nullable=False)

    # Metadata
    color = Column(String(20), nullable=True)  # Hex color for UI
    icon = Column(String(50), nullable=True)  # Icon name

    # Counts (denormalized for performance)
    workflow_count = Column(Integer, default=0)
    subfolder_count = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    parent = relationship("Folder", remote_side=[id], back_populates="subfolders")
    subfolders = relationship(
        "Folder",
        back_populates="parent",
        cascade="all, delete-orphan",
    )
    user = relationship("User")
