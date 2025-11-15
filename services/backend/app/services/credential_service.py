"""Credential management service - Secure storage for API keys, OAuth tokens, and secrets"""

from __future__ import annotations

import asyncio
import base64
import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import os

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.logging import get_logger
from app.db.models.user import User

logger = get_logger(__name__)


class CredentialType:
    """Credential type constants"""
    API_KEY = "api_key"
    OAUTH_TOKEN = "oauth_token"
    PASSWORD = "password"
    CERTIFICATE = "certificate"
    SECRET = "secret"
    CONNECTION_STRING = "connection_string"


@dataclass
class Credential:
    """Credential record"""
    id: str
    name: str
    type: str
    service: str  # e.g., "slack", "openai", "github"
    user_id: str
    workspace_id: Optional[str]
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    metadata: dict[str, Any] = field(default_factory=dict)

    # Encrypted value (not exposed in API responses)
    _encrypted_value: Optional[str] = None


class CredentialService:
    """
    Manages encrypted credentials for integrations

    Features:
    - Encryption at rest using Fernet (AES-128)
    - Per-user credential isolation
    - Workspace-level credentials
    - Automatic expiration handling
    - OAuth token refresh support
    """

    def __init__(self):
        self._credentials: dict[str, Credential] = {}
        self._lock = asyncio.Lock()
        self._cipher = self._initialize_cipher()

    def _initialize_cipher(self) -> Fernet:
        """Initialize encryption cipher"""
        # Get encryption key from environment or generate one
        encryption_key = os.getenv("CREDENTIAL_ENCRYPTION_KEY")

        if not encryption_key:
            # In production, this should ALWAYS be set via environment variable
            # For development, we'll generate a key (data won't persist across restarts)
            logger.warning("CREDENTIAL_ENCRYPTION_KEY not set - generating temporary key")
            encryption_key = Fernet.generate_key().decode()

        # Ensure key is properly formatted
        if isinstance(encryption_key, str):
            encryption_key = encryption_key.encode()

        try:
            return Fernet(encryption_key)
        except Exception as e:
            logger.error(f"Failed to initialize cipher: {e}")
            # Fallback to a generated key
            return Fernet(Fernet.generate_key())

    async def store_credential(
        self,
        *,
        name: str,
        service: str,
        credential_type: str,
        value: str | dict[str, Any],
        user_id: str,
        workspace_id: Optional[str] = None,
        expires_in_days: Optional[int] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> Credential:
        """
        Store a new credential

        Args:
            name: Human-readable name for the credential
            service: Service identifier (e.g., "slack", "openai")
            credential_type: Type of credential (api_key, oauth_token, etc.)
            value: The actual credential value (will be encrypted)
            user_id: User who owns this credential
            workspace_id: Optional workspace scope
            expires_in_days: Optional expiration in days
            metadata: Additional metadata (e.g., scopes, permissions)
        """
        credential_id = f"{service}_{user_id}_{name}".replace(" ", "_")

        # Serialize value if it's a dict (for OAuth tokens with refresh tokens, etc.)
        if isinstance(value, dict):
            value_str = json.dumps(value)
        else:
            value_str = value

        # Encrypt the credential value
        encrypted_value = self._cipher.encrypt(value_str.encode()).decode()

        # Calculate expiration
        expires_at = None
        if expires_in_days:
            expires_at = datetime.utcnow() + timedelta(days=expires_in_days)

        credential = Credential(
            id=credential_id,
            name=name,
            type=credential_type,
            service=service,
            user_id=user_id,
            workspace_id=workspace_id,
            expires_at=expires_at,
            metadata=metadata or {},
            _encrypted_value=encrypted_value,
        )

        async with self._lock:
            self._credentials[credential_id] = credential

        logger.info(
            "credential_stored",
            credential_id=credential_id,
            service=service,
            user_id=user_id,
            type=credential_type,
        )

        return credential

    async def get_credential(
        self,
        *,
        credential_id: Optional[str] = None,
        service: Optional[str] = None,
        user_id: str,
        workspace_id: Optional[str] = None,
        decrypt: bool = True,
    ) -> Optional[str | dict[str, Any]]:
        """
        Retrieve and decrypt a credential

        Args:
            credential_id: Specific credential ID
            service: Service name to look up default credential
            user_id: User who owns the credential
            workspace_id: Optional workspace scope
            decrypt: Whether to decrypt the value

        Returns:
            Decrypted credential value or None if not found
        """
        async with self._lock:
            # Find credential by ID or by service
            credential = None

            if credential_id:
                credential = self._credentials.get(credential_id)
            elif service:
                # Find first matching credential for service and user
                for cred in self._credentials.values():
                    if (
                        cred.service == service
                        and cred.user_id == user_id
                        and (workspace_id is None or cred.workspace_id == workspace_id)
                    ):
                        credential = cred
                        break

            if not credential:
                return None

            # Check authorization
            if credential.user_id != user_id:
                logger.warning(
                    "credential_access_denied",
                    credential_id=credential.id,
                    requesting_user=user_id,
                    owner=credential.user_id,
                )
                return None

            # Check expiration
            if credential.expires_at and credential.expires_at < datetime.utcnow():
                logger.info("credential_expired", credential_id=credential.id)
                return None

            if not decrypt or not credential._encrypted_value:
                return None

            # Decrypt the value
            try:
                decrypted_bytes = self._cipher.decrypt(credential._encrypted_value.encode())
                decrypted_str = decrypted_bytes.decode()

                # Try to parse as JSON (for OAuth tokens)
                try:
                    return json.loads(decrypted_str)
                except json.JSONDecodeError:
                    return decrypted_str

            except Exception as e:
                logger.error(
                    "credential_decryption_failed",
                    credential_id=credential.id,
                    error=str(e),
                )
                return None

    async def list_credentials(
        self,
        *,
        user_id: str,
        workspace_id: Optional[str] = None,
        service: Optional[str] = None,
    ) -> list[dict[str, Any]]:
        """
        List credentials (without decrypting values)

        Returns metadata about credentials without exposing values
        """
        async with self._lock:
            credentials = [
                cred
                for cred in self._credentials.values()
                if cred.user_id == user_id
                and (workspace_id is None or cred.workspace_id == workspace_id)
                and (service is None or cred.service == service)
            ]

        return [
            {
                "id": cred.id,
                "name": cred.name,
                "type": cred.type,
                "service": cred.service,
                "workspace_id": cred.workspace_id,
                "created_at": cred.created_at.isoformat(),
                "updated_at": cred.updated_at.isoformat(),
                "expires_at": cred.expires_at.isoformat() if cred.expires_at else None,
                "is_expired": cred.expires_at < datetime.utcnow() if cred.expires_at else False,
                "metadata": cred.metadata,
            }
            for cred in credentials
        ]

    async def update_credential(
        self,
        *,
        credential_id: str,
        user_id: str,
        value: Optional[str | dict[str, Any]] = None,
        metadata: Optional[dict[str, Any]] = None,
        expires_in_days: Optional[int] = None,
    ) -> bool:
        """Update an existing credential"""
        async with self._lock:
            credential = self._credentials.get(credential_id)

            if not credential or credential.user_id != user_id:
                return False

            # Update value if provided
            if value is not None:
                if isinstance(value, dict):
                    value_str = json.dumps(value)
                else:
                    value_str = value

                encrypted_value = self._cipher.encrypt(value_str.encode()).decode()
                credential._encrypted_value = encrypted_value

            # Update metadata
            if metadata is not None:
                credential.metadata.update(metadata)

            # Update expiration
            if expires_in_days is not None:
                credential.expires_at = datetime.utcnow() + timedelta(days=expires_in_days)

            credential.updated_at = datetime.utcnow()

        logger.info("credential_updated", credential_id=credential_id, user_id=user_id)
        return True

    async def delete_credential(
        self,
        *,
        credential_id: str,
        user_id: str,
    ) -> bool:
        """Delete a credential"""
        async with self._lock:
            credential = self._credentials.get(credential_id)

            if not credential or credential.user_id != user_id:
                return False

            del self._credentials[credential_id]

        logger.info("credential_deleted", credential_id=credential_id, user_id=user_id)
        return True

    async def rotate_credential(
        self,
        *,
        credential_id: str,
        new_value: str | dict[str, Any],
        user_id: str,
    ) -> bool:
        """
        Rotate a credential (update value and reset expiration)

        Useful for periodic credential rotation policies
        """
        return await self.update_credential(
            credential_id=credential_id,
            user_id=user_id,
            value=new_value,
            expires_in_days=90,  # Default 90-day rotation
        )

    async def validate_credential(
        self,
        *,
        service: str,
        user_id: str,
        workspace_id: Optional[str] = None,
    ) -> tuple[bool, Optional[str]]:
        """
        Check if a valid credential exists for a service

        Returns:
            (is_valid, error_message)
        """
        credential_value = await self.get_credential(
            service=service,
            user_id=user_id,
            workspace_id=workspace_id,
        )

        if not credential_value:
            return False, f"No credential found for {service}"

        # Could add service-specific validation here
        # e.g., make a test API call to verify the credential

        return True, None


# Singleton instance
credential_service = CredentialService()
