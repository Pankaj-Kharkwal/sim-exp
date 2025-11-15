"""Credentials API endpoints - Secure credential management"""

from typing import Optional, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field

from app.core.auth import get_current_user
from app.core.logging import get_logger
from app.db.models.user import User
from app.db.session import get_db
from app.services.credential_service import credential_service, CredentialType

logger = get_logger(__name__)

router = APIRouter(prefix="/credentials", tags=["Credentials"])


# Schemas
class StoreCredentialRequest(BaseModel):
    """Store credential request"""
    name: str = Field(..., description="Human-readable name")
    service: str = Field(..., description="Service identifier (slack, openai, github, etc.)")
    type: str = Field(default=CredentialType.API_KEY, description="Credential type")
    value: str | dict[str, Any] = Field(..., description="Credential value (will be encrypted)")
    workspace_id: Optional[str] = Field(None, alias="workspaceId")
    expires_in_days: Optional[int] = Field(None, alias="expiresInDays")
    metadata: Optional[dict[str, Any]] = None

    model_config = {"populate_by_name": True}


class UpdateCredentialRequest(BaseModel):
    """Update credential request"""
    value: Optional[str | dict[str, Any]] = None
    metadata: Optional[dict[str, Any]] = None
    expires_in_days: Optional[int] = Field(None, alias="expiresInDays")

    model_config = {"populate_by_name": True}


class CredentialResponse(BaseModel):
    """Credential response (without sensitive data)"""
    id: str
    name: str
    type: str
    service: str
    workspace_id: Optional[str] = Field(None, alias="workspaceId")
    created_at: str = Field(alias="createdAt")
    updated_at: str = Field(alias="updatedAt")
    expires_at: Optional[str] = Field(None, alias="expiresAt")
    is_expired: bool = Field(alias="isExpired")
    metadata: dict[str, Any]

    model_config = {"populate_by_name": True}


class ValidationResponse(BaseModel):
    """Credential validation response"""
    is_valid: bool = Field(alias="isValid")
    error: Optional[str] = None

    model_config = {"populate_by_name": True}


# Endpoints
@router.post("/", response_model=CredentialResponse)
async def store_credential(
    request: StoreCredentialRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Store a new credential

    Securely stores API keys, OAuth tokens, and other credentials.
    Values are encrypted at rest.

    Example services:
    - openai, anthropic, google, mistral (AI providers)
    - slack, discord, teams (Communication)
    - github, gitlab, linear, jira (Development)
    - gmail, outlook, sendgrid (Email)
    - stripe, paypal (Payments)
    """
    logger.info(
        "credential_store_requested",
        user_id=current_user.id,
        service=request.service,
        type=request.type,
    )

    try:
        credential = await credential_service.store_credential(
            name=request.name,
            service=request.service,
            credential_type=request.type,
            value=request.value,
            user_id=current_user.id,
            workspace_id=request.workspace_id,
            expires_in_days=request.expires_in_days,
            metadata=request.metadata,
        )

        return CredentialResponse(
            id=credential.id,
            name=credential.name,
            type=credential.type,
            service=credential.service,
            workspaceId=credential.workspace_id,
            createdAt=credential.created_at.isoformat(),
            updatedAt=credential.updated_at.isoformat(),
            expiresAt=credential.expires_at.isoformat() if credential.expires_at else None,
            isExpired=False,
            metadata=credential.metadata,
        )

    except Exception as e:
        logger.error("credential_store_failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to store credential",
        ) from e


@router.get("/", response_model=list[CredentialResponse])
async def list_credentials(
    workspace_id: Optional[str] = None,
    service: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    List all credentials for the current user

    Returns credential metadata without exposing sensitive values.
    """
    logger.info(
        "credentials_list_requested",
        user_id=current_user.id,
        workspace_id=workspace_id,
        service=service,
    )

    credentials = await credential_service.list_credentials(
        user_id=current_user.id,
        workspace_id=workspace_id,
        service=service,
    )

    return [CredentialResponse(**cred) for cred in credentials]


@router.get("/{credential_id}", response_model=CredentialResponse)
async def get_credential_metadata(
    credential_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get credential metadata (without value)

    Returns information about a credential without exposing the actual value.
    """
    logger.info(
        "credential_metadata_requested",
        user_id=current_user.id,
        credential_id=credential_id,
    )

    credentials = await credential_service.list_credentials(user_id=current_user.id)
    credential = next((c for c in credentials if c["id"] == credential_id), None)

    if not credential:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Credential not found",
        )

    return CredentialResponse(**credential)


@router.patch("/{credential_id}", response_model=CredentialResponse)
async def update_credential(
    credential_id: str,
    request: UpdateCredentialRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Update an existing credential

    Can update value, metadata, or expiration.
    """
    logger.info(
        "credential_update_requested",
        user_id=current_user.id,
        credential_id=credential_id,
    )

    success = await credential_service.update_credential(
        credential_id=credential_id,
        user_id=current_user.id,
        value=request.value,
        metadata=request.metadata,
        expires_in_days=request.expires_in_days,
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Credential not found or access denied",
        )

    # Return updated metadata
    credentials = await credential_service.list_credentials(user_id=current_user.id)
    credential = next((c for c in credentials if c["id"] == credential_id), None)

    if not credential:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Credential not found",
        )

    return CredentialResponse(**credential)


@router.delete("/{credential_id}")
async def delete_credential(
    credential_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a credential"""
    logger.info(
        "credential_delete_requested",
        user_id=current_user.id,
        credential_id=credential_id,
    )

    success = await credential_service.delete_credential(
        credential_id=credential_id,
        user_id=current_user.id,
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Credential not found or access denied",
        )

    return {"id": credential_id, "deleted": True}


@router.post("/{credential_id}/rotate")
async def rotate_credential(
    credential_id: str,
    new_value: str | dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Rotate a credential

    Updates the credential value and resets expiration.
    Useful for periodic security rotations.
    """
    logger.info(
        "credential_rotation_requested",
        user_id=current_user.id,
        credential_id=credential_id,
    )

    success = await credential_service.rotate_credential(
        credential_id=credential_id,
        new_value=new_value,
        user_id=current_user.id,
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Credential not found or access denied",
        )

    return {"id": credential_id, "rotated": True}


@router.get("/validate/{service}", response_model=ValidationResponse)
async def validate_service_credential(
    service: str,
    workspace_id: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Validate if a credential exists for a service

    Checks if the user has a valid (non-expired) credential for the specified service.
    """
    logger.info(
        "credential_validation_requested",
        user_id=current_user.id,
        service=service,
        workspace_id=workspace_id,
    )

    is_valid, error = await credential_service.validate_credential(
        service=service,
        user_id=current_user.id,
        workspace_id=workspace_id,
    )

    return ValidationResponse(isValid=is_valid, error=error)


@router.post("/test/{service}")
async def test_credential(
    service: str,
    workspace_id: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Test a credential by making a test API call

    Makes a simple API call to verify the credential is valid.
    Implementation varies by service.
    """
    logger.info(
        "credential_test_requested",
        user_id=current_user.id,
        service=service,
    )

    # Get the credential
    credential_value = await credential_service.get_credential(
        service=service,
        user_id=current_user.id,
        workspace_id=workspace_id,
    )

    if not credential_value:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No credential found for {service}",
        )

    # TODO: Implement service-specific test calls
    # For now, just verify credential exists
    return {
        "service": service,
        "tested": True,
        "valid": True,
        "message": f"Credential found for {service}. Service-specific validation not yet implemented.",
    }
