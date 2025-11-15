"""Knowledge Base Database Models"""

from datetime import datetime
from typing import Optional
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
    Float,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
import uuid

from app.db.base import Base


class KnowledgeBase(Base):
    """Knowledge Base collection"""

    __tablename__ = "knowledge_bases"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    user_id = Column(String, ForeignKey("user.id"), nullable=True)
    organization_id = Column(
        String, ForeignKey("organization.id"), nullable=True
    )

    # Settings
    embedding_model = Column(String(100), default="text-embedding-ada-002")
    chunk_size = Column(Integer, default=1000)
    chunk_overlap = Column(Integer, default=200)
    is_public = Column(Boolean, default=False)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    documents = relationship(
        "Document",
        back_populates="knowledge_base",
        cascade="all, delete-orphan",
    )
    user = relationship("User", back_populates="knowledge_bases")


class Document(Base):
    """Document in a knowledge base"""

    __tablename__ = "documents"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    knowledge_base_id = Column(
        String, ForeignKey("knowledge_bases.id"), nullable=False
    )

    # Document info
    name = Column(String(500), nullable=False)
    file_path = Column(String(1000), nullable=True)  # Cloud storage path
    file_type = Column(String(50), nullable=False)  # pdf, docx, txt, etc.
    file_size = Column(Integer, nullable=True)  # bytes

    # Content
    content = Column(Text, nullable=True)  # Extracted text content
    document_metadata = Column("metadata", JSONB, nullable=True)  # Custom metadata (renamed from metadata to avoid SQLAlchemy reserved name)

    # Processing status
    status = Column(
        String(50),
        default="pending",
    )  # pending, processing, completed, failed
    error_message = Column(Text, nullable=True)

    # Tags
    tags = Column(ARRAY(String), nullable=True, default=[])

    # Statistics
    chunk_count = Column(Integer, default=0)
    character_count = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)

    # Relationships
    knowledge_base = relationship("KnowledgeBase", back_populates="documents")
    chunks = relationship(
        "DocumentChunk",
        back_populates="document",
        cascade="all, delete-orphan",
    )


class DocumentChunk(Base):
    """Chunk of a document with embeddings"""

    __tablename__ = "document_chunks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String, ForeignKey("documents.id"), nullable=False)

    # Chunk info
    chunk_index = Column(Integer, nullable=False)  # Order in document
    content = Column(Text, nullable=False)  # The actual text chunk

    # Embeddings
    embedding = Column(ARRAY(Float), nullable=True)  # Vector embedding
    embedding_model = Column(String(100), nullable=True)

    # Metadata
    chunk_metadata = Column("metadata", JSONB, nullable=True)  # Custom metadata (renamed to avoid SQLAlchemy reserved name)
    character_count = Column(Integer, nullable=False)
    token_count = Column(Integer, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    document = relationship("Document", back_populates="chunks")


class TagDefinition(Base):
    """Tag definitions for knowledge base"""

    __tablename__ = "tag_definitions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    knowledge_base_id = Column(
        String, ForeignKey("knowledge_bases.id"), nullable=False
    )

    name = Column(String(100), nullable=False)
    color = Column(String(20), nullable=True)
    description = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
