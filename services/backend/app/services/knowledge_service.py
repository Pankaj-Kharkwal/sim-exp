"""Knowledge Base Service

Handles document management, chunking, and semantic search
"""

from typing import List, Optional, Tuple
from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.logging import get_logger
from app.db.models.knowledge import (
    KnowledgeBase,
    Document,
    DocumentChunk,
    TagDefinition,
)
from app.schemas.knowledge import (
    KnowledgeBaseCreate,
    KnowledgeBaseUpdate,
    DocumentCreate,
    DocumentUpdate,
    DocumentChunkCreate,
    SemanticSearchRequest,
    SearchResult,
)

logger = get_logger(__name__)


class KnowledgeBaseService:
    """Service for managing knowledge bases"""

    async def list_knowledge_bases(
        self,
        user_id: str,
        organization_id: str,
        skip: int = 0,
        limit: int = 100,
        include_public: bool = True,
        db: AsyncSession = None,
    ) -> Tuple[List[KnowledgeBase], int]:
        """List knowledge bases for a user"""
        logger.info("list_knowledge_bases", user_id=user_id, skip=skip, limit=limit)

        # Build query
        query = select(KnowledgeBase).options(
            selectinload(KnowledgeBase.documents)
        )

        # Filter by organization or public
        if include_public:
            query = query.where(
                or_(
                    KnowledgeBase.organization_id == organization_id,
                    KnowledgeBase.is_public == True,
                )
            )
        else:
            query = query.where(
                KnowledgeBase.organization_id == organization_id
            )

        # Count total
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar()

        # Apply pagination
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        knowledge_bases = result.scalars().all()

        return knowledge_bases, total

    async def get_knowledge_base(
        self,
        kb_id: str,
        db: AsyncSession,
        include_documents: bool = False,
    ) -> Optional[KnowledgeBase]:
        """Get knowledge base by ID"""
        logger.info("get_knowledge_base", kb_id=kb_id)

        query = select(KnowledgeBase).where(KnowledgeBase.id == kb_id)

        if include_documents:
            query = query.options(selectinload(KnowledgeBase.documents))

        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def create_knowledge_base(
        self,
        user_id: str,
        organization_id: str,
        kb_data: KnowledgeBaseCreate,
        db: AsyncSession,
    ) -> KnowledgeBase:
        """Create a new knowledge base"""
        from datetime import datetime
        logger.info("create_knowledge_base", name=kb_data.name, user_id=user_id)

        now = datetime.utcnow()
        kb = KnowledgeBase(
            name=kb_data.name,
            description=kb_data.description,
            user_id=user_id,
            organization_id=organization_id,
            embedding_model=kb_data.embedding_model,
            chunk_size=kb_data.chunk_size,
            chunk_overlap=kb_data.chunk_overlap,
            is_public=kb_data.is_public,
            created_at=now,
            updated_at=now,
        )

        db.add(kb)
        await db.commit()
        await db.refresh(kb)

        logger.info("knowledge_base_created", kb_id=kb.id)
        return kb

    async def update_knowledge_base(
        self,
        kb_id: str,
        kb_data: KnowledgeBaseUpdate,
        db: AsyncSession,
    ) -> Optional[KnowledgeBase]:
        """Update knowledge base"""
        logger.info("update_knowledge_base", kb_id=kb_id)

        kb = await self.get_knowledge_base(kb_id, db)
        if not kb:
            return None

        # Update fields
        update_data = kb_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(kb, field, value)

        await db.commit()
        await db.refresh(kb)

        logger.info("knowledge_base_updated", kb_id=kb_id)
        return kb

    async def delete_knowledge_base(
        self, kb_id: str, db: AsyncSession
    ) -> bool:
        """Delete knowledge base and all documents"""
        logger.info("delete_knowledge_base", kb_id=kb_id)

        kb = await self.get_knowledge_base(kb_id, db)
        if not kb:
            return False

        await db.delete(kb)
        await db.commit()

        logger.info("knowledge_base_deleted", kb_id=kb_id)
        return True


class DocumentService:
    """Service for managing documents"""

    async def list_documents(
        self,
        kb_id: str,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        tags: Optional[List[str]] = None,
        search: Optional[str] = None,
        db: AsyncSession = None,
    ) -> Tuple[List[Document], int]:
        """List documents in a knowledge base"""
        logger.info("list_documents", kb_id=kb_id, skip=skip, limit=limit)

        query = select(Document).where(Document.knowledge_base_id == kb_id)

        # Filter by status
        if status:
            query = query.where(Document.status == status)

        # Filter by tags
        if tags:
            query = query.where(Document.tags.overlap(tags))

        # Search by name
        if search:
            query = query.where(Document.name.ilike(f"%{search}%"))

        # Count total
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar()

        # Apply pagination and ordering
        query = query.order_by(Document.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(query)
        documents = result.scalars().all()

        return documents, total

    async def get_document(
        self,
        document_id: str,
        db: AsyncSession,
        include_chunks: bool = False,
    ) -> Optional[Document]:
        """Get document by ID"""
        logger.info("get_document", document_id=document_id)

        query = select(Document).where(Document.id == document_id)

        if include_chunks:
            query = query.options(selectinload(Document.chunks))

        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def create_document(
        self,
        kb_id: str,
        doc_data: DocumentCreate,
        db: AsyncSession,
    ) -> Document:
        """Create a new document"""
        logger.info("create_document", name=doc_data.name, kb_id=kb_id)

        doc = Document(
            knowledge_base_id=kb_id,
            name=doc_data.name,
            file_path=doc_data.file_path,
            file_type=doc_data.file_type,
            file_size=doc_data.file_size,
            content=doc_data.content,
            metadata=doc_data.metadata,
            tags=doc_data.tags or [],
            character_count=len(doc_data.content) if doc_data.content else 0,
            status="pending",
        )

        db.add(doc)
        await db.commit()
        await db.refresh(doc)

        logger.info("document_created", document_id=doc.id)
        return doc

    async def update_document(
        self,
        document_id: str,
        doc_data: DocumentUpdate,
        db: AsyncSession,
    ) -> Optional[Document]:
        """Update document"""
        logger.info("update_document", document_id=document_id)

        doc = await self.get_document(document_id, db)
        if not doc:
            return None

        # Update fields
        update_data = doc_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(doc, field, value)

        # Update character count if content changed
        if doc_data.content is not None:
            doc.character_count = len(doc_data.content)

        await db.commit()
        await db.refresh(doc)

        logger.info("document_updated", document_id=document_id)
        return doc

    async def delete_document(
        self, document_id: str, db: AsyncSession
    ) -> bool:
        """Delete document and all chunks"""
        logger.info("delete_document", document_id=document_id)

        doc = await self.get_document(document_id, db)
        if not doc:
            return False

        await db.delete(doc)
        await db.commit()

        logger.info("document_deleted", document_id=document_id)
        return True

    async def create_chunks(
        self,
        document_id: str,
        chunks: List[DocumentChunkCreate],
        db: AsyncSession,
    ) -> List[DocumentChunk]:
        """Create chunks for a document"""
        logger.info("create_chunks", document_id=document_id, count=len(chunks))

        chunk_objs = [
            DocumentChunk(
                document_id=document_id,
                chunk_index=chunk.chunk_index,
                content=chunk.content,
                embedding=chunk.embedding,
                embedding_model=chunk.embedding_model,
                metadata=chunk.metadata,
                character_count=chunk.character_count,
                token_count=chunk.token_count,
            )
            for chunk in chunks
        ]

        db.add_all(chunk_objs)

        # Update document chunk count
        doc = await self.get_document(document_id, db)
        if doc:
            doc.chunk_count = len(chunk_objs)
            doc.status = "completed"

        await db.commit()

        logger.info("chunks_created", document_id=document_id, count=len(chunk_objs))
        return chunk_objs

    async def semantic_search(
        self,
        kb_id: str,
        search_request: SemanticSearchRequest,
        db: AsyncSession,
    ) -> List[SearchResult]:
        """Perform semantic search on knowledge base

        Note: This is a placeholder. In production, use:
        - pgvector for PostgreSQL vector search
        - Pinecone, Weaviate, or Qdrant for dedicated vector databases
        """
        logger.info("semantic_search", kb_id=kb_id, query=search_request.query)

        # TODO: Implement actual semantic search with embeddings
        # For now, do simple text search
        query = (
            select(DocumentChunk, Document)
            .join(Document)
            .where(Document.knowledge_base_id == kb_id)
            .where(DocumentChunk.content.ilike(f"%{search_request.query}%"))
            .limit(search_request.top_k)
        )

        # Apply tag filters if provided
        if search_request.filter_tags:
            query = query.where(Document.tags.overlap(search_request.filter_tags))

        result = await db.execute(query)
        rows = result.all()

        # Format results
        results = [
            SearchResult(
                chunk_id=chunk.id,
                document_id=chunk.document_id,
                document_name=doc.name,
                content=chunk.content,
                similarity=0.8,  # Placeholder
                metadata=chunk.metadata,
                chunk_index=chunk.chunk_index,
            )
            for chunk, doc in rows
        ]

        logger.info("semantic_search_complete", results_count=len(results))
        return results
