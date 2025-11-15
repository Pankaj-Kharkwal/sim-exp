"""In-memory chat and chatbot deployment service."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.logging import get_logger
from app.db.models import Workflow
from app.db.models.user import User
from app.services.workflow_service import WorkflowService

from openai import AsyncAzureOpenAI

logger = get_logger(__name__)


@dataclass
class ChatMessageRecord:
    """Stored chat message."""

    role: str
    content: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ConversationState:
    """Conversation container."""

    id: str
    user_id: str
    workflow_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    messages: list[ChatMessageRecord] = field(default_factory=list)


@dataclass
class ChatbotDeployment:
    """Deployed chatbot metadata."""

    id: str
    identifier: str
    workflow_id: str
    title: str
    description: Optional[str]
    chatbot_url: str
    welcome_message: str
    owner_id: str
    created_at: datetime = field(default_factory=datetime.utcnow)


class ChatService:
    """Manages chat conversations and chatbot deployments."""

    def __init__(self) -> None:
        self._conversations: dict[str, ConversationState] = {}
        self._deployments: dict[str, ChatbotDeployment] = {}
        self._lock = asyncio.Lock()
        self._workflow_service = WorkflowService()

        # Initialize Azure OpenAI client
        self._azure_client = None
        if settings.AZURE_OPENAI_ENDPOINT and settings.AZURE_OPENAI_API_KEY:
            self._azure_client = AsyncAzureOpenAI(
                azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
                api_key=settings.AZURE_OPENAI_API_KEY,
                api_version=settings.AZURE_OPENAI_API_VERSION,
            )
            logger.info("Azure OpenAI client initialized successfully")

    async def send_message(
        self,
        *,
        request_message: str,
        requested_conversation_id: Optional[str],
        workflow_id: Optional[str],
        user: User,
        db: AsyncSession,
    ) -> tuple[str, str, dict[str, Any]]:
        """Record a user message and generate a deterministic assistant reply."""

        conversation_id = requested_conversation_id or str(uuid.uuid4())

        async with self._lock:
            conversation = self._conversations.get(conversation_id)
            if not conversation:
                conversation = ConversationState(
                    id=conversation_id,
                    user_id=user.id,
                    workflow_id=workflow_id,
                )
                self._conversations[conversation_id] = conversation
            else:
                if workflow_id and not conversation.workflow_id:
                    conversation.workflow_id = workflow_id

            conversation.messages.append(
                ChatMessageRecord(role="user", content=request_message)
            )
            conversation.updated_at = datetime.utcnow()

        workflow_summary = await self._build_workflow_summary(
            workflow_id or conversation.workflow_id, user, db
        )

        reply = await self._compose_reply(
            message=request_message,
            conversation=conversation,
            workflow_summary=workflow_summary,
        )

        metadata: dict[str, Any] = {
            "conversation": {
                "messageCount": len(conversation.messages) + 1,  # include assistant reply
                "createdAt": conversation.created_at.isoformat(),
            },
            "workflow": workflow_summary,
        }

        async with self._lock:
            conversation.messages.append(
                ChatMessageRecord(role="assistant", content=reply, metadata=metadata)
            )
            conversation.updated_at = datetime.utcnow()

        logger.info(
            "chat_message_processed",
            conversation_id=conversation_id,
            user_id=user.id,
            workflow_id=conversation.workflow_id,
        )

        return conversation_id, reply, metadata

    async def _build_workflow_summary(
        self, workflow_id: Optional[str], user: User, db: AsyncSession
    ) -> Optional[dict[str, Any]]:
        """Load workflow metadata for responses."""
        if not workflow_id:
            return None

        workflow = await self._workflow_service.get_workflow(
            workflow_id, db, include_blocks=True, include_edges=True
        )
        if not workflow:
            return {"status": "not_found", "workflowId": workflow_id}

        return {
            "workflowId": workflow_id,
            "name": workflow.name,
            "ownerId": workflow.user_id,
            "blockCount": len(workflow.blocks),
            "edgeCount": len(workflow.edges),
            "canExecute": workflow.user_id == user.id,
        }

    async def _compose_reply(
        self,
        *,
        message: str,
        conversation: ConversationState,
        workflow_summary: Optional[dict[str, Any]],
    ) -> str:
        """Create a contextual assistant reply using Azure OpenAI."""

        # If Azure OpenAI is not configured, fall back to stub response
        if not self._azure_client:
            logger.warning("Azure OpenAI not configured, using stub response")
            return f"I captured your request and logged it for follow-up. You said: \"{message.strip()}\"."

        try:
            # Build conversation history for context
            messages = [
                {
                    "role": "system",
                    "content": "You are Pankh AI Assistant, a helpful AI that helps users with workflow automation and general tasks. Be concise, friendly, and helpful."
                }
            ]

            # Add workflow context if available
            if workflow_summary and workflow_summary.get("status") != "not_found":
                context = f"The user has access to a workflow named '{workflow_summary.get('name')}' with {workflow_summary.get('blockCount')} blocks."
                messages.append({
                    "role": "system",
                    "content": context
                })

            # Add conversation history (last 10 messages for context)
            for msg in conversation.messages[-10:]:
                messages.append({
                    "role": msg.role,
                    "content": msg.content
                })

            # Add current user message
            messages.append({
                "role": "user",
                "content": message
            })

            # Call Azure OpenAI
            response = await self._azure_client.chat.completions.create(
                model=settings.AZURE_OPENAI_DEPLOYMENT_CHAT,
                messages=messages,
                # temperature not supported by gpt-5-mini (defaults to 1)
                max_completion_tokens=500,  # GPT-5 uses max_completion_tokens instead of max_tokens
            )

            reply = response.choices[0].message.content or ""
            logger.info(
                "Azure OpenAI response generated",
                tokens=response.usage.total_tokens,
                reply_length=len(reply),
                finish_reason=response.choices[0].finish_reason
            )

            if not reply:
                logger.warning("Azure OpenAI returned empty content", response_dict=response.model_dump())
                return "I received your message but couldn't generate a response. Please try again."

            return reply

        except Exception as e:
            logger.error("Azure OpenAI error", error=str(e))
            # Fallback to stub response on error
            return f"I'm having trouble connecting to my AI service right now. Your message was: \"{message.strip()}\". Please try again in a moment."

    async def get_history(self, conversation_id: str) -> Optional[ConversationState]:
        """Return a conversation if present."""
        async with self._lock:
            return self._conversations.get(conversation_id)

    async def delete_conversation(self, conversation_id: str) -> bool:
        """Delete conversation if present."""
        async with self._lock:
            existed = self._conversations.pop(conversation_id, None)
        return existed is not None

    async def deploy_chatbot(
        self,
        *,
        workflow_id: str,
        identifier: str,
        title: str,
        description: Optional[str],
        welcome_message: str,
        user: User,
        db: AsyncSession,
    ) -> ChatbotDeployment:
        """Register a chatbot deployment in-memory."""
        workflow = await self._workflow_service.get_workflow(
            workflow_id, db, include_blocks=False, include_edges=False
        )
        if not workflow:
            raise ValueError("Workflow not found")

        async with self._lock:
            if identifier in self._deployments:
                raise ValueError("Identifier already in use")

            deployment = ChatbotDeployment(
                id=str(uuid.uuid4()),
                identifier=identifier,
                workflow_id=workflow_id,
                title=title,
                description=description,
                chatbot_url=f"{settings.FRONTEND_URL.rstrip('/')}/chat/{identifier}",
                welcome_message=welcome_message,
                owner_id=user.id,
            )
            self._deployments[identifier] = deployment

        logger.info(
            "chatbot_deployed",
            deployment_id=deployment.id,
            workflow_id=workflow_id,
            identifier=identifier,
        )

        return deployment

    async def list_deployments(self) -> list[ChatbotDeployment]:
        """Return all deployments (primarily for debugging)."""
        async with self._lock:
            return list(self._deployments.values())


# Shared service instance
chat_service = ChatService()
