"""Storage Service

Handles file uploads, downloads, and storage operations.
Supports multiple storage backends: Local, Azure Blob, AWS S3
"""

import os
import uuid
from typing import Optional, BinaryIO, Tuple
from pathlib import Path
import aiofiles

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class StorageService:
    """Service for file storage operations"""

    def __init__(self):
        self.storage_type = getattr(settings, "STORAGE_TYPE", "local")
        self.local_storage_path = Path(getattr(settings, "LOCAL_STORAGE_PATH", "./storage"))
        self.local_storage_path.mkdir(parents=True, exist_ok=True)

    async def upload_file(
        self,
        file_content: bytes,
        filename: str,
        content_type: Optional[str] = None,
        folder: str = "uploads",
    ) -> Tuple[str, str]:
        """
        Upload a file to storage

        Args:
            file_content: File content as bytes
            filename: Original filename
            content_type: MIME type
            folder: Folder/prefix for the file

        Returns:
            Tuple of (file_id, file_url)
        """
        # Generate unique file ID
        file_id = str(uuid.uuid4())
        file_ext = Path(filename).suffix
        stored_filename = f"{file_id}{file_ext}"

        if self.storage_type == "local":
            return await self._upload_local(
                file_content, stored_filename, folder
            )
        elif self.storage_type == "azure":
            return await self._upload_azure(
                file_content, stored_filename, folder, content_type
            )
        elif self.storage_type == "s3":
            return await self._upload_s3(
                file_content, stored_filename, folder, content_type
            )
        else:
            raise ValueError(f"Unsupported storage type: {self.storage_type}")

    async def _upload_local(
        self,
        file_content: bytes,
        filename: str,
        folder: str,
    ) -> Tuple[str, str]:
        """Upload file to local storage"""
        logger.info("upload_local", filename=filename, folder=folder)

        # Create folder if doesn't exist
        folder_path = self.local_storage_path / folder
        folder_path.mkdir(parents=True, exist_ok=True)

        # Write file
        file_path = folder_path / filename
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(file_content)

        # Generate URL (relative path)
        file_url = f"/files/{folder}/{filename}"

        logger.info("file_uploaded_locally", file_path=str(file_path))
        return filename, file_url

    async def _upload_azure(
        self,
        file_content: bytes,
        filename: str,
        folder: str,
        content_type: Optional[str] = None,
    ) -> Tuple[str, str]:
        """Upload file to Azure Blob Storage"""
        try:
            from azure.storage.blob.aio import BlobServiceClient
            from azure.identity.aio import DefaultAzureCredential

            logger.info("upload_azure", filename=filename, folder=folder)

            # Get connection string or use managed identity
            connection_string = getattr(settings, "AZURE_STORAGE_CONNECTION_STRING", None)
            container_name = getattr(settings, "AZURE_STORAGE_CONTAINER", "uploads")

            if connection_string:
                blob_service_client = BlobServiceClient.from_connection_string(
                    connection_string
                )
            else:
                # Use managed identity
                account_url = getattr(settings, "AZURE_STORAGE_ACCOUNT_URL")
                credential = DefaultAzureCredential()
                blob_service_client = BlobServiceClient(
                    account_url=account_url,
                    credential=credential
                )

            # Upload blob
            blob_name = f"{folder}/{filename}"
            blob_client = blob_service_client.get_blob_client(
                container=container_name,
                blob=blob_name
            )

            await blob_client.upload_blob(
                file_content,
                content_type=content_type,
                overwrite=True
            )

            # Get URL
            file_url = blob_client.url

            logger.info("file_uploaded_azure", blob_name=blob_name, url=file_url)
            return filename, file_url

        except ImportError:
            logger.error("azure_storage_not_installed")
            raise RuntimeError("Azure storage libraries not installed")

    async def _upload_s3(
        self,
        file_content: bytes,
        filename: str,
        folder: str,
        content_type: Optional[str] = None,
    ) -> Tuple[str, str]:
        """Upload file to AWS S3"""
        try:
            import aioboto3

            logger.info("upload_s3", filename=filename, folder=folder)

            bucket_name = getattr(settings, "AWS_S3_BUCKET", "uploads")
            region = getattr(settings, "AWS_REGION", "us-east-1")

            session = aioboto3.Session()
            async with session.client(
                's3',
                region_name=region,
                aws_access_key_id=getattr(settings, "AWS_ACCESS_KEY_ID", None),
                aws_secret_access_key=getattr(settings, "AWS_SECRET_ACCESS_KEY", None),
            ) as s3_client:
                # Upload file
                key = f"{folder}/{filename}"
                extra_args = {}
                if content_type:
                    extra_args['ContentType'] = content_type

                await s3_client.put_object(
                    Bucket=bucket_name,
                    Key=key,
                    Body=file_content,
                    **extra_args
                )

                # Generate URL
                file_url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{key}"

                logger.info("file_uploaded_s3", key=key, url=file_url)
                return filename, file_url

        except ImportError:
            logger.error("boto3_not_installed")
            raise RuntimeError("AWS boto3 library not installed")

    async def download_file(
        self,
        file_path: str,
    ) -> Optional[bytes]:
        """
        Download a file from storage

        Args:
            file_path: Path to the file (URL or local path)

        Returns:
            File content as bytes, or None if not found
        """
        if self.storage_type == "local":
            return await self._download_local(file_path)
        elif self.storage_type == "azure":
            return await self._download_azure(file_path)
        elif self.storage_type == "s3":
            return await self._download_s3(file_path)
        else:
            raise ValueError(f"Unsupported storage type: {self.storage_type}")

    async def _download_local(self, file_path: str) -> Optional[bytes]:
        """Download file from local storage"""
        logger.info("download_local", file_path=file_path)

        # Remove /files/ prefix if present
        if file_path.startswith("/files/"):
            file_path = file_path[7:]

        full_path = self.local_storage_path / file_path

        if not full_path.exists():
            logger.warning("file_not_found", file_path=str(full_path))
            return None

        async with aiofiles.open(full_path, 'rb') as f:
            content = await f.read()

        logger.info("file_downloaded_locally", size=len(content))
        return content

    async def _download_azure(self, blob_url: str) -> Optional[bytes]:
        """Download file from Azure Blob Storage"""
        try:
            from azure.storage.blob.aio import BlobServiceClient
            from azure.identity.aio import DefaultAzureCredential

            logger.info("download_azure", blob_url=blob_url)

            connection_string = getattr(settings, "AZURE_STORAGE_CONNECTION_STRING", None)

            if connection_string:
                blob_service_client = BlobServiceClient.from_connection_string(
                    connection_string
                )
            else:
                account_url = getattr(settings, "AZURE_STORAGE_ACCOUNT_URL")
                credential = DefaultAzureCredential()
                blob_service_client = BlobServiceClient(
                    account_url=account_url,
                    credential=credential
                )

            # Parse blob URL to get container and blob name
            # Simplified - assumes standard Azure URL format
            blob_client = blob_service_client.get_blob_client_from_url(blob_url)

            # Download blob
            downloader = await blob_client.download_blob()
            content = await downloader.readall()

            logger.info("file_downloaded_azure", size=len(content))
            return content

        except ImportError:
            logger.error("azure_storage_not_installed")
            raise RuntimeError("Azure storage libraries not installed")

    async def _download_s3(self, s3_key: str) -> Optional[bytes]:
        """Download file from AWS S3"""
        try:
            import aioboto3

            logger.info("download_s3", s3_key=s3_key)

            bucket_name = getattr(settings, "AWS_S3_BUCKET", "uploads")
            region = getattr(settings, "AWS_REGION", "us-east-1")

            session = aioboto3.Session()
            async with session.client(
                's3',
                region_name=region,
                aws_access_key_id=getattr(settings, "AWS_ACCESS_KEY_ID", None),
                aws_secret_access_key=getattr(settings, "AWS_SECRET_ACCESS_KEY", None),
            ) as s3_client:
                # Download file
                response = await s3_client.get_object(
                    Bucket=bucket_name,
                    Key=s3_key
                )

                content = await response['Body'].read()

                logger.info("file_downloaded_s3", size=len(content))
                return content

        except ImportError:
            logger.error("boto3_not_installed")
            raise RuntimeError("AWS boto3 library not installed")

    async def delete_file(self, file_path: str) -> bool:
        """
        Delete a file from storage

        Args:
            file_path: Path to the file

        Returns:
            True if deleted successfully, False otherwise
        """
        if self.storage_type == "local":
            return await self._delete_local(file_path)
        elif self.storage_type == "azure":
            return await self._delete_azure(file_path)
        elif self.storage_type == "s3":
            return await self._delete_s3(file_path)
        else:
            raise ValueError(f"Unsupported storage type: {self.storage_type}")

    async def _delete_local(self, file_path: str) -> bool:
        """Delete file from local storage"""
        logger.info("delete_local", file_path=file_path)

        if file_path.startswith("/files/"):
            file_path = file_path[7:]

        full_path = self.local_storage_path / file_path

        if not full_path.exists():
            logger.warning("file_not_found", file_path=str(full_path))
            return False

        full_path.unlink()
        logger.info("file_deleted_locally", file_path=str(full_path))
        return True

    async def _delete_azure(self, blob_url: str) -> bool:
        """Delete file from Azure Blob Storage"""
        try:
            from azure.storage.blob.aio import BlobServiceClient
            from azure.identity.aio import DefaultAzureCredential

            logger.info("delete_azure", blob_url=blob_url)

            connection_string = getattr(settings, "AZURE_STORAGE_CONNECTION_STRING", None)

            if connection_string:
                blob_service_client = BlobServiceClient.from_connection_string(
                    connection_string
                )
            else:
                account_url = getattr(settings, "AZURE_STORAGE_ACCOUNT_URL")
                credential = DefaultAzureCredential()
                blob_service_client = BlobServiceClient(
                    account_url=account_url,
                    credential=credential
                )

            blob_client = blob_service_client.get_blob_client_from_url(blob_url)
            await blob_client.delete_blob()

            logger.info("file_deleted_azure")
            return True

        except ImportError:
            logger.error("azure_storage_not_installed")
            raise RuntimeError("Azure storage libraries not installed")

    async def _delete_s3(self, s3_key: str) -> bool:
        """Delete file from AWS S3"""
        try:
            import aioboto3

            logger.info("delete_s3", s3_key=s3_key)

            bucket_name = getattr(settings, "AWS_S3_BUCKET", "uploads")
            region = getattr(settings, "AWS_REGION", "us-east-1")

            session = aioboto3.Session()
            async with session.client(
                's3',
                region_name=region,
                aws_access_key_id=getattr(settings, "AWS_ACCESS_KEY_ID", None),
                aws_secret_access_key=getattr(settings, "AWS_SECRET_ACCESS_KEY", None),
            ) as s3_client:
                await s3_client.delete_object(
                    Bucket=bucket_name,
                    Key=s3_key
                )

                logger.info("file_deleted_s3")
                return True

        except ImportError:
            logger.error("boto3_not_installed")
            raise RuntimeError("AWS boto3 library not installed")

    async def get_presigned_upload_url(
        self,
        filename: str,
        content_type: Optional[str] = None,
        folder: str = "uploads",
        expiration: int = 3600,
    ) -> dict:
        """
        Generate a presigned URL for direct upload to storage

        Args:
            filename: Name of the file
            content_type: MIME type
            folder: Folder/prefix
            expiration: URL expiration in seconds

        Returns:
            Dict with upload_url, file_id, and other metadata
        """
        file_id = str(uuid.uuid4())
        file_ext = Path(filename).suffix
        stored_filename = f"{file_id}{file_ext}"

        if self.storage_type == "azure":
            return await self._get_azure_presigned_url(
                stored_filename, folder, content_type, expiration
            )
        elif self.storage_type == "s3":
            return await self._get_s3_presigned_url(
                stored_filename, folder, content_type, expiration
            )
        else:
            # Local storage doesn't support presigned URLs
            return {
                "error": "Presigned URLs not supported for local storage",
                "use_direct_upload": True,
            }

    async def _get_azure_presigned_url(
        self,
        filename: str,
        folder: str,
        content_type: Optional[str],
        expiration: int,
    ) -> dict:
        """Generate Azure Blob Storage SAS URL"""
        try:
            from azure.storage.blob import generate_blob_sas, BlobSasPermissions
            from datetime import datetime, timedelta

            container_name = getattr(settings, "AZURE_STORAGE_CONTAINER", "uploads")
            account_name = getattr(settings, "AZURE_STORAGE_ACCOUNT_NAME")
            account_key = getattr(settings, "AZURE_STORAGE_ACCOUNT_KEY")

            blob_name = f"{folder}/{filename}"

            sas_token = generate_blob_sas(
                account_name=account_name,
                container_name=container_name,
                blob_name=blob_name,
                account_key=account_key,
                permission=BlobSasPermissions(write=True),
                expiry=datetime.utcnow() + timedelta(seconds=expiration)
            )

            upload_url = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"

            return {
                "upload_url": upload_url,
                "file_id": filename,
                "blob_name": blob_name,
                "expires_in": expiration,
            }

        except ImportError:
            raise RuntimeError("Azure storage libraries not installed")

    async def _get_s3_presigned_url(
        self,
        filename: str,
        folder: str,
        content_type: Optional[str],
        expiration: int,
    ) -> dict:
        """Generate S3 presigned URL"""
        try:
            import aioboto3

            bucket_name = getattr(settings, "AWS_S3_BUCKET", "uploads")
            region = getattr(settings, "AWS_REGION", "us-east-1")
            key = f"{folder}/{filename}"

            session = aioboto3.Session()
            async with session.client(
                's3',
                region_name=region,
                aws_access_key_id=getattr(settings, "AWS_ACCESS_KEY_ID", None),
                aws_secret_access_key=getattr(settings, "AWS_SECRET_ACCESS_KEY", None),
            ) as s3_client:
                params = {
                    'Bucket': bucket_name,
                    'Key': key,
                }
                if content_type:
                    params['ContentType'] = content_type

                upload_url = await s3_client.generate_presigned_url(
                    'put_object',
                    Params=params,
                    ExpiresIn=expiration
                )

                return {
                    "upload_url": upload_url,
                    "file_id": filename,
                    "key": key,
                    "expires_in": expiration,
                }

        except ImportError:
            raise RuntimeError("AWS boto3 library not installed")
