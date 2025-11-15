"""Chat API endpoints - AI conversation interface"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field

from app.core.auth import get_current_user
from app.core.logging import get_logger
from app.db.models.user import User
from app.db.session import get_db
from app.services.chat_service import chat_service

logger = get_logger(__name__)

router = APIRouter(prefix="/chat", tags=["Chat"])


# Schemas
class ChatMessage(BaseModel):
    """Chat message schema"""
    role: str = Field(..., description="Message role: user, assistant, system")
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    """Chat request schema"""
    message: str = Field(..., description="User message")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for context")
    workflow_id: Optional[str] = Field(None, alias="workflowId", description="Workflow to execute")
    stream: bool = Field(default=False, description="Stream response")
    model: Optional[str] = Field(default="gpt-4", description="AI model to use")

    model_config = {"populate_by_name": True}


class ChatResponse(BaseModel):
    """Chat response schema"""
    conversation_id: str = Field(alias="conversationId")
    message: str
    role: str = "assistant"
    metadata: Optional[dict] = None

    model_config = {"populate_by_name": True}


class ChatbotDeployRequest(BaseModel):
    """Chatbot deployment request"""
    workflow_id: str = Field(alias="workflowId")
    identifier: str = Field(..., min_length=1, description="Unique chatbot identifier")
    title: str
    description: Optional[str] = None
    welcome_message: str = Field(alias="welcomeMessage")
    primary_color: Optional[str] = Field(default="#3972F6", alias="primaryColor")
    image_url: Optional[str] = Field(None, alias="imageUrl")
    auth_type: str = Field(default="public", alias="authType")  # public, password, email
    password: Optional[str] = None
    allowed_emails: list[str] = Field(default_factory=list, alias="allowedEmails")

    model_config = {"populate_by_name": True}


class ChatbotResponse(BaseModel):
    """Chatbot deployment response"""
    id: str
    chatbot_url: str = Field(alias="chatbotUrl")
    identifier: str
    title: str
    workflow_id: str = Field(alias="workflowId")

    model_config = {"populate_by_name": True}


class ConversationHistoryResponse(BaseModel):
    """Conversation history response"""

    conversation_id: str = Field(alias="conversationId")
    workflow_id: Optional[str] = Field(default=None, alias="workflowId")
    messages: list[ChatMessage]
    created_at: str = Field(alias="createdAt")
    updated_at: str = Field(alias="updatedAt")

    model_config = {"populate_by_name": True}


# Endpoints
@router.post("/", response_model=ChatResponse)
async def send_chat_message(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Send a chat message and get AI response

    This endpoint handles:
    - Regular AI chat conversations
    - Workflow execution via chat
    - Conversation context management
    """
    logger.info(
        "chat_message_received",
        user_id=current_user.id,
        conversation_id=request.conversation_id,
        workflow_id=request.workflow_id,
    )

    conversation_id, reply, metadata = await chat_service.send_message(
        request_message=request.message,
        requested_conversation_id=request.conversation_id,
        workflow_id=request.workflow_id,
        user=current_user,
        db=db,
    )

    return ChatResponse(
        conversationId=conversation_id,
        message=reply,
        metadata=metadata,
    )


@router.post("/deploy", response_model=ChatbotResponse)
async def deploy_chatbot(
    request: ChatbotDeployRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Deploy a workflow as a chatbot

    Creates a publicly accessible chatbot interface for a workflow.
    Similar to the Sim app's chat deployment feature.
    """
    logger.info(
        "chatbot_deploy_requested",
        user_id=current_user.id,
        workflow_id=request.workflow_id,
        identifier=request.identifier,
    )

    try:
        deployment = await chat_service.deploy_chatbot(
            workflow_id=request.workflow_id,
            identifier=request.identifier,
            title=request.title,
            description=request.description,
            welcome_message=request.welcome_message,
            user=current_user,
            db=db,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return ChatbotResponse(
        id=deployment.id,
        chatbotUrl=deployment.chatbot_url,
        identifier=deployment.identifier,
        title=deployment.title,
        workflowId=deployment.workflow_id,
    )


@router.get("/{conversation_id}/history", response_model=ConversationHistoryResponse)
async def get_conversation_history(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get conversation history"""
    logger.info(
        "conversation_history_requested",
        user_id=current_user.id,
        conversation_id=conversation_id,
    )

    conversation = await chat_service.get_history(conversation_id)
    if not conversation or conversation.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    return ConversationHistoryResponse(
        conversationId=conversation.id,
        workflowId=conversation.workflow_id,
        createdAt=conversation.created_at.isoformat(),
        updatedAt=conversation.updated_at.isoformat(),
        messages=[
            ChatMessage(role=message.role, content=message.content)
            for message in conversation.messages
        ],
    )


@router.delete("/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a conversation"""
    logger.info(
        "conversation_delete_requested",
        user_id=current_user.id,
        conversation_id=conversation_id,
    )

    deleted = await chat_service.delete_conversation(conversation_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    return {"conversationId": conversation_id, "deleted": True}
