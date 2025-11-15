from typing import Any, Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.db.models import User
from app.db.session import get_db
from app.schemas.billing import BillingData
from app.services.billing_service import billing_service

router = APIRouter()


@router.get("", response_model=BillingData)
async def get_billing_data(
    context: Literal["user", "organization"] = Query("user"),
    context_id: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Unified Billing Endpoint
    """
    if context == "user":
        summary = await billing_service.get_user_billing(current_user, db)
    elif context == "organization":
        if not context_id:
            raise HTTPException(
                status_code=400,
                detail="Organization ID is required when context=organization",
            )
        try:
            summary = await billing_service.get_organization_billing(
                organization_id=context_id, user=current_user, db=db
            )
        except PermissionError as exc:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(exc),
            ) from exc
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            ) from exc
    else:
        raise HTTPException(status_code=400, detail="Unknown billing context")

    return BillingData(success=True, context=context, data=summary)
