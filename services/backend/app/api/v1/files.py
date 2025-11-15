"""Files API Endpoints

Handles file uploads, downloads, and storage operations
"""

from typing import Optional, List
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    UploadFile,
    File,
    Query,
    Body,
)
from fastapi.responses import StreamingResponse, Response
from sqlalchemy.ext.asyncio import AsyncSession
import io

from app.core.logging import get_logger
from app.db.session import get_db
from app.services.storage_service import StorageService

router = APIRouter()
logger = get_logger(__name__)


def get_current_user_id() -> str:
    """Get current user ID - placeholder"""
    return "demo-user-id"


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    folder: str = Query("uploads", description="Folder to store the file"),
    db: AsyncSession = Depends(get_db),
):
    """
    Upload a file to storage

    Args:
        file: The file to upload
        folder: Optional folder name (default: uploads)

    Returns:
        File metadata including file_id and file_url
    """
    logger.info("upload_file", filename=file.filename, content_type=file.content_type)

    try:
        # Read file content
        file_content = await file.read()
        file_size = len(file_content)

        # Upload to storage
        storage_service = StorageService()
        file_id, file_url = await storage_service.upload_file(
            file_content=file_content,
            filename=file.filename,
            content_type=file.content_type,
            folder=folder,
        )

        logger.info(
            "file_uploaded",
            file_id=file_id,
            filename=file.filename,
            size=file_size,
        )

        return {
            "file_id": file_id,
            "filename": file.filename,
            "file_url": file_url,
            "content_type": file.content_type,
            "size": file_size,
            "folder": folder,
        }

    except Exception as e:
        logger.error("file_upload_failed", error=str(e), filename=file.filename)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"File upload failed: {str(e)}",
        )


@router.post("/upload/batch", status_code=status.HTTP_201_CREATED)
async def upload_multiple_files(
    files: List[UploadFile] = File(...),
    folder: str = Query("uploads", description="Folder to store the files"),
    db: AsyncSession = Depends(get_db),
):
    """
    Upload multiple files at once

    Args:
        files: List of files to upload
        folder: Optional folder name (default: uploads)

    Returns:
        List of file metadata
    """
    logger.info("upload_multiple_files", count=len(files), folder=folder)

    storage_service = StorageService()
    results = []

    for file in files:
        try:
            # Read file content
            file_content = await file.read()
            file_size = len(file_content)

            # Upload to storage
            file_id, file_url = await storage_service.upload_file(
                file_content=file_content,
                filename=file.filename,
                content_type=file.content_type,
                folder=folder,
            )

            results.append({
                "file_id": file_id,
                "filename": file.filename,
                "file_url": file_url,
                "content_type": file.content_type,
                "size": file_size,
                "folder": folder,
                "status": "success",
            })

            logger.info("file_uploaded_in_batch", file_id=file_id, filename=file.filename)

        except Exception as e:
            logger.error("file_upload_failed_in_batch", error=str(e), filename=file.filename)
            results.append({
                "filename": file.filename,
                "status": "failed",
                "error": str(e),
            })

    return {
        "files": results,
        "total": len(files),
        "successful": len([r for r in results if r.get("status") == "success"]),
        "failed": len([r for r in results if r.get("status") == "failed"]),
    }


@router.get("/download")
async def download_file(
    file_path: str = Query(..., description="Path to the file"),
    db: AsyncSession = Depends(get_db),
):
    """
    Download a file from storage

    Args:
        file_path: Path or URL of the file to download

    Returns:
        File content as streaming response
    """
    logger.info("download_file", file_path=file_path)

    try:
        storage_service = StorageService()
        file_content = await storage_service.download_file(file_path)

        if file_content is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"File not found: {file_path}",
            )

        # Extract filename from path
        filename = file_path.split("/")[-1]

        # Return as streaming response
        return StreamingResponse(
            io.BytesIO(file_content),
            media_type="application/octet-stream",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("file_download_failed", error=str(e), file_path=file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"File download failed: {str(e)}",
        )


@router.delete("/delete")
async def delete_file(
    file_path: str = Query(..., description="Path to the file"),
    db: AsyncSession = Depends(get_db),
):
    """
    Delete a file from storage

    Args:
        file_path: Path or URL of the file to delete

    Returns:
        Deletion confirmation
    """
    logger.info("delete_file", file_path=file_path)

    try:
        storage_service = StorageService()
        success = await storage_service.delete_file(file_path)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"File not found: {file_path}",
            )

        logger.info("file_deleted", file_path=file_path)

        return {
            "success": True,
            "message": "File deleted successfully",
            "file_path": file_path,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("file_delete_failed", error=str(e), file_path=file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"File deletion failed: {str(e)}",
        )


@router.post("/presigned")
async def get_presigned_upload_url(
    filename: str = Body(..., embed=True),
    content_type: Optional[str] = Body(None, embed=True),
    folder: str = Body("uploads", embed=True),
    expiration: int = Body(3600, embed=True, description="Expiration in seconds"),
    db: AsyncSession = Depends(get_db),
):
    """
    Get a presigned URL for direct file upload to cloud storage

    This allows clients to upload directly to Azure/S3 without going through the backend.

    Args:
        filename: Name of the file to upload
        content_type: MIME type of the file
        folder: Folder to store the file
        expiration: How long the URL should be valid (seconds)

    Returns:
        Presigned URL and metadata
    """
    logger.info("get_presigned_upload_url", filename=filename, folder=folder)

    try:
        storage_service = StorageService()
        presigned_data = await storage_service.get_presigned_upload_url(
            filename=filename,
            content_type=content_type,
            folder=folder,
            expiration=expiration,
        )

        logger.info("presigned_url_generated", filename=filename)

        return presigned_data

    except Exception as e:
        logger.error("presigned_url_generation_failed", error=str(e), filename=filename)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate presigned URL: {str(e)}",
        )


@router.get("/serve/{path:path}")
async def serve_file(
    path: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Serve a file directly (for local storage)

    This endpoint serves files from local storage.
    For cloud storage, use the direct URLs instead.

    Args:
        path: Path to the file relative to storage root

    Returns:
        File content
    """
    logger.info("serve_file", path=path)

    try:
        storage_service = StorageService()
        file_content = await storage_service.download_file(path)

        if file_content is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"File not found: {path}",
            )

        # Determine content type based on extension
        content_type = "application/octet-stream"
        if path.endswith(".pdf"):
            content_type = "application/pdf"
        elif path.endswith((".jpg", ".jpeg")):
            content_type = "image/jpeg"
        elif path.endswith(".png"):
            content_type = "image/png"
        elif path.endswith(".txt"):
            content_type = "text/plain"
        elif path.endswith(".json"):
            content_type = "application/json"

        return Response(
            content=file_content,
            media_type=content_type,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("file_serve_failed", error=str(e), path=path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to serve file: {str(e)}",
        )
