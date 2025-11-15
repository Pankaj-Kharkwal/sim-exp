"""Knowledge Base API Endpoints"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Body, Query, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.core.auth import get_current_user
from app.db.session import get_db
from app.db.models.user import User
from app.db.models.organization import OrganizationMember
from sqlalchemy import select
from app.schemas.knowledge import (
    KnowledgeBaseCreate,
    KnowledgeBaseUpdate,
    KnowledgeBaseResponse,
    KnowledgeBaseListResponse,
    DocumentCreate,
    DocumentUpdate,
    DocumentResponse,
    DocumentListResponse,
    DocumentChunkCreate,
    DocumentChunkResponse,
    DocumentChunkListResponse,
    SemanticSearchRequest,
    SemanticSearchResponse,
    TagDefinitionCreate,
    TagDefinitionResponse,
    TagDefinitionListResponse,
)
from app.services.knowledge_service import (
    KnowledgeBaseService,
    DocumentService,
)

router = APIRouter()
logger = get_logger(__name__)


async def get_user_organization_id(user_id: str, db: AsyncSession) -> Optional[str]:
    """Get the user's first organization ID"""
    query = select(OrganizationMember.organization_id).where(
        OrganizationMember.user_id == user_id
    ).limit(1)
    result = await db.execute(query)
    org_id = result.scalar_one_or_none()
    return org_id


# Knowledge Base Endpoints
@router.get("/", response_model=KnowledgeBaseListResponse)
async def list_knowledge_bases(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    include_public: bool = Query(True),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all knowledge bases"""
    logger.info("list_knowledge_bases", skip=skip, limit=limit)

    org_id = await get_user_organization_id(current_user.id, db)
    if not org_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must belong to an organization. Please create an organization first."
        )

    service = KnowledgeBaseService()
    kbs, total = await service.list_knowledge_bases(
        user_id=current_user.id,
        organization_id=org_id,
        skip=skip,
        limit=limit,
        include_public=include_public,
        db=db,
    )

    return KnowledgeBaseListResponse(
        knowledge_bases=[
            KnowledgeBaseResponse(
                id=kb.id,
                name=kb.name,
                description=kb.description,
                user_id=kb.user_id,
                organization_id=kb.organization_id,
                embedding_model=kb.embedding_model,
                chunk_size=kb.chunk_size,
                chunk_overlap=kb.chunk_overlap,
                is_public=kb.is_public,
                created_at=kb.created_at,
                updated_at=kb.updated_at,
                document_count=len(kb.documents) if hasattr(kb, 'documents') else 0,
                chunk_count=0,  # TODO: Calculate
            )
            for kb in kbs
        ],
        total=total,
        skip=skip,
        limit=limit,
    )


@router.post("/", response_model=KnowledgeBaseResponse, status_code=status.HTTP_201_CREATED)
async def create_knowledge_base(
    kb_data: KnowledgeBaseCreate = Body(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new knowledge base"""
    logger.info("create_knowledge_base", name=kb_data.name)

    org_id = await get_user_organization_id(current_user.id, db)
    if not org_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must belong to an organization. Please create an organization first."
        )

    service = KnowledgeBaseService()
    kb = await service.create_knowledge_base(
        user_id=current_user.id,
        organization_id=org_id,
        kb_data=kb_data,
        db=db,
    )

    return KnowledgeBaseResponse(
        id=kb.id,
        name=kb.name,
        description=kb.description,
        user_id=kb.user_id,
        organization_id=kb.organization_id,
        embedding_model=kb.embedding_model,
        chunk_size=kb.chunk_size,
        chunk_overlap=kb.chunk_overlap,
        is_public=kb.is_public,
        created_at=kb.created_at,
        updated_at=kb.updated_at,
        document_count=0,
        chunk_count=0,
    )


@router.get("/{kb_id}", response_model=KnowledgeBaseResponse)
async def get_knowledge_base(
    kb_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Get knowledge base by ID"""
    logger.info("get_knowledge_base", kb_id=kb_id)

    service = KnowledgeBaseService()
    kb = await service.get_knowledge_base(kb_id, db, include_documents=True)

    if not kb:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Knowledge base not found: {kb_id}",
        )

    return KnowledgeBaseResponse(
        id=kb.id,
        name=kb.name,
        description=kb.description,
        user_id=kb.user_id,
        organization_id=kb.organization_id,
        embedding_model=kb.embedding_model,
        chunk_size=kb.chunk_size,
        chunk_overlap=kb.chunk_overlap,
        is_public=kb.is_public,
        created_at=kb.created_at,
        updated_at=kb.updated_at,
        document_count=len(kb.documents) if hasattr(kb, 'documents') else 0,
        chunk_count=sum(doc.chunk_count for doc in kb.documents) if hasattr(kb, 'documents') else 0,
    )


@router.put("/{kb_id}", response_model=KnowledgeBaseResponse)
async def update_knowledge_base(
    kb_id: str,
    kb_data: KnowledgeBaseUpdate = Body(...),
    db: AsyncSession = Depends(get_db),
):
    """Update knowledge base"""
    logger.info("update_knowledge_base", kb_id=kb_id)

    service = KnowledgeBaseService()
    kb = await service.update_knowledge_base(kb_id, kb_data, db)

    if not kb:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Knowledge base not found: {kb_id}",
        )

    return KnowledgeBaseResponse(
        id=kb.id,
        name=kb.name,
        description=kb.description,
        user_id=kb.user_id,
        organization_id=kb.organization_id,
        embedding_model=kb.embedding_model,
        chunk_size=kb.chunk_size,
        chunk_overlap=kb.chunk_overlap,
        is_public=kb.is_public,
        created_at=kb.created_at,
        updated_at=kb.updated_at,
        document_count=0,
        chunk_count=0,
    )


@router.delete("/{kb_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_knowledge_base(
    kb_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Delete knowledge base"""
    logger.info("delete_knowledge_base", kb_id=kb_id)

    service = KnowledgeBaseService()
    success = await service.delete_knowledge_base(kb_id, db)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Knowledge base not found: {kb_id}",
        )

    return None


# Document Endpoints
@router.get("/{kb_id}/documents", response_model=DocumentListResponse)
async def list_documents(
    kb_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """List documents in a knowledge base"""
    logger.info("list_documents", kb_id=kb_id, skip=skip, limit=limit)

    service = DocumentService()
    docs, total = await service.list_documents(
        kb_id=kb_id,
        skip=skip,
        limit=limit,
        status=status,
        search=search,
        db=db,
    )

    return DocumentListResponse(
        documents=[
            DocumentResponse(
                id=doc.id,
                knowledge_base_id=doc.knowledge_base_id,
                name=doc.name,
                file_path=doc.file_path,
                file_type=doc.file_type,
                file_size=doc.file_size,
                status=doc.status,
                error_message=doc.error_message,
                tags=doc.tags or [],
                chunk_count=doc.chunk_count,
                character_count=doc.character_count,
                metadata=doc.metadata,
                created_at=doc.created_at,
                updated_at=doc.updated_at,
                processed_at=doc.processed_at,
            )
            for doc in docs
        ],
        total=total,
        skip=skip,
        limit=limit,
    )


@router.post("/{kb_id}/documents", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_document(
    kb_id: str,
    doc_data: DocumentCreate = Body(...),
    db: AsyncSession = Depends(get_db),
):
    """Create a new document in the knowledge base"""
    logger.info("create_document", kb_id=kb_id, name=doc_data.name)

    service = DocumentService()
    doc = await service.create_document(kb_id, doc_data, db)

    return DocumentResponse(
        id=doc.id,
        knowledge_base_id=doc.knowledge_base_id,
        name=doc.name,
        file_path=doc.file_path,
        file_type=doc.file_type,
        file_size=doc.file_size,
        status=doc.status,
        error_message=doc.error_message,
        tags=doc.tags or [],
        chunk_count=doc.chunk_count,
        character_count=doc.character_count,
        metadata=doc.metadata,
        created_at=doc.created_at,
        updated_at=doc.updated_at,
        processed_at=doc.processed_at,
    )


@router.get("/{kb_id}/documents/{document_id}", response_model=DocumentResponse)
async def get_document(
    kb_id: str,
    document_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Get document by ID"""
    logger.info("get_document", kb_id=kb_id, document_id=document_id)

    service = DocumentService()
    doc = await service.get_document(document_id, db)

    if not doc or doc.knowledge_base_id != kb_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document not found: {document_id}",
        )

    return DocumentResponse(
        id=doc.id,
        knowledge_base_id=doc.knowledge_base_id,
        name=doc.name,
        file_path=doc.file_path,
        file_type=doc.file_type,
        file_size=doc.file_size,
        status=doc.status,
        error_message=doc.error_message,
        tags=doc.tags or [],
        chunk_count=doc.chunk_count,
        character_count=doc.character_count,
        metadata=doc.metadata,
        created_at=doc.created_at,
        updated_at=doc.updated_at,
        processed_at=doc.processed_at,
    )


@router.put("/{kb_id}/documents/{document_id}", response_model=DocumentResponse)
async def update_document(
    kb_id: str,
    document_id: str,
    doc_data: DocumentUpdate = Body(...),
    db: AsyncSession = Depends(get_db),
):
    """Update document"""
    logger.info("update_document", kb_id=kb_id, document_id=document_id)

    service = DocumentService()
    doc = await service.update_document(document_id, doc_data, db)

    if not doc or doc.knowledge_base_id != kb_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document not found: {document_id}",
        )

    return DocumentResponse(
        id=doc.id,
        knowledge_base_id=doc.knowledge_base_id,
        name=doc.name,
        file_path=doc.file_path,
        file_type=doc.file_type,
        file_size=doc.file_size,
        status=doc.status,
        error_message=doc.error_message,
        tags=doc.tags or [],
        chunk_count=doc.chunk_count,
        character_count=doc.character_count,
        metadata=doc.metadata,
        created_at=doc.created_at,
        updated_at=doc.updated_at,
        processed_at=doc.processed_at,
    )


@router.delete("/{kb_id}/documents/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    kb_id: str,
    document_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Delete document"""
    logger.info("delete_document", kb_id=kb_id, document_id=document_id)

    service = DocumentService()
    success = await service.delete_document(document_id, db)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document not found: {document_id}",
        )

    return None


# Semantic Search Endpoint
@router.post("/{kb_id}/search", response_model=SemanticSearchResponse)
async def semantic_search(
    kb_id: str,
    search_request: SemanticSearchRequest = Body(...),
    db: AsyncSession = Depends(get_db),
):
    """Perform semantic search on knowledge base"""
    logger.info("semantic_search", kb_id=kb_id, query=search_request.query)

    service = DocumentService()
    results = await service.semantic_search(kb_id, search_request, db)

    return SemanticSearchResponse(
        results=results,
        query=search_request.query,
        total_results=len(results),
    )


# Chunk Endpoints
@router.post("/{kb_id}/documents/{document_id}/chunks", response_model=List[DocumentChunkResponse])
async def create_document_chunks(
    kb_id: str,
    document_id: str,
    chunks: List[DocumentChunkCreate] = Body(...),
    db: AsyncSession = Depends(get_db),
):
    """Create chunks for a document"""
    logger.info("create_document_chunks", document_id=document_id, count=len(chunks))

    service = DocumentService()
    chunk_objs = await service.create_chunks(document_id, chunks, db)

    return [
        DocumentChunkResponse(
            id=chunk.id,
            document_id=chunk.document_id,
            chunk_index=chunk.chunk_index,
            content=chunk.content,
            embedding_model=chunk.embedding_model,
            metadata=chunk.metadata,
            character_count=chunk.character_count,
            token_count=chunk.token_count,
            created_at=chunk.created_at,
        )
        for chunk in chunk_objs
    ]
