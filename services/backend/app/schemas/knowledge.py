"""Knowledge Base Pydantic Schemas"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


# Knowledge Base Schemas
class KnowledgeBaseCreate(BaseModel):
    """Schema for creating a knowledge base"""

    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    embedding_model: str = "text-embedding-ada-002"
    chunk_size: int = Field(default=1000, ge=100, le=4000)
    chunk_overlap: int = Field(default=200, ge=0, le=1000)
    is_public: bool = False


class KnowledgeBaseUpdate(BaseModel):
    """Schema for updating a knowledge base"""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    embedding_model: Optional[str] = None
    chunk_size: Optional[int] = Field(None, ge=100, le=4000)
    chunk_overlap: Optional[int] = Field(None, ge=0, le=1000)
    is_public: Optional[bool] = None


class KnowledgeBaseResponse(BaseModel):
    """Schema for knowledge base response"""

    id: str
    name: str
    description: Optional[str]
    user_id: str
    organization_id: str
    embedding_model: str
    chunk_size: int
    chunk_overlap: int
    is_public: bool
    created_at: datetime
    updated_at: datetime
    document_count: Optional[int] = 0
    chunk_count: Optional[int] = 0

    class Config:
        from_attributes = True


class KnowledgeBaseListResponse(BaseModel):
    """Schema for list of knowledge bases"""

    knowledge_bases: List[KnowledgeBaseResponse]
    total: int
    skip: int
    limit: int


# Document Schemas
class DocumentCreate(BaseModel):
    """Schema for creating a document"""

    name: str = Field(..., min_length=1, max_length=500)
    file_path: Optional[str] = None
    file_type: str
    file_size: Optional[int] = None
    content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = []


class DocumentUpdate(BaseModel):
    """Schema for updating a document"""

    name: Optional[str] = Field(None, min_length=1, max_length=500)
    content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    status: Optional[str] = None


class DocumentResponse(BaseModel):
    """Schema for document response"""

    id: str
    knowledge_base_id: str
    name: str
    file_path: Optional[str]
    file_type: str
    file_size: Optional[int]
    status: str
    error_message: Optional[str]
    tags: List[str]
    chunk_count: int
    character_count: int
    metadata: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime
    processed_at: Optional[datetime]

    class Config:
        from_attributes = True


class DocumentListResponse(BaseModel):
    """Schema for list of documents"""

    documents: List[DocumentResponse]
    total: int
    skip: int
    limit: int


# Chunk Schemas
class DocumentChunkCreate(BaseModel):
    """Schema for creating a document chunk"""

    chunk_index: int
    content: str
    embedding: Optional[List[float]] = None
    embedding_model: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    character_count: int
    token_count: Optional[int] = None


class DocumentChunkResponse(BaseModel):
    """Schema for document chunk response"""

    id: str
    document_id: str
    chunk_index: int
    content: str
    embedding_model: Optional[str]
    metadata: Optional[Dict[str, Any]]
    character_count: int
    token_count: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


class DocumentChunkListResponse(BaseModel):
    """Schema for list of document chunks"""

    chunks: List[DocumentChunkResponse]
    total: int
    skip: int
    limit: int


# Search Schemas
class SemanticSearchRequest(BaseModel):
    """Schema for semantic search request"""

    query: str = Field(..., min_length=1)
    top_k: int = Field(default=5, ge=1, le=50)
    min_similarity: float = Field(default=0.7, ge=0.0, le=1.0)
    filter_tags: Optional[List[str]] = None


class SearchResult(BaseModel):
    """Schema for a single search result"""

    chunk_id: str
    document_id: str
    document_name: str
    content: str
    similarity: float
    metadata: Optional[Dict[str, Any]]
    chunk_index: int


class SemanticSearchResponse(BaseModel):
    """Schema for semantic search response"""

    results: List[SearchResult]
    query: str
    total_results: int


# Tag Schemas
class TagDefinitionCreate(BaseModel):
    """Schema for creating a tag definition"""

    name: str = Field(..., min_length=1, max_length=100)
    color: Optional[str] = None
    description: Optional[str] = None


class TagDefinitionResponse(BaseModel):
    """Schema for tag definition response"""

    id: str
    knowledge_base_id: str
    name: str
    color: Optional[str]
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TagDefinitionListResponse(BaseModel):
    """Schema for list of tag definitions"""

    tags: List[TagDefinitionResponse]
    total: int
