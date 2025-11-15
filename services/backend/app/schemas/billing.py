"""Billing schemas"""

from typing import Any, Optional
from pydantic import BaseModel, Field


class BillingData(BaseModel):
    """Billing data response schema"""

    success: bool = True
    context: str
    data: dict[str, Any] = Field(default_factory=dict)


class UsageData(BaseModel):
    """Usage tracking data"""

    executions: int = 0
    api_calls: int = 0
    storage_gb: float = 0.0
    credits_used: float = 0.0
    credits_remaining: Optional[float] = None


class SubscriptionData(BaseModel):
    """Subscription information"""

    plan: str = "free"
    status: str = "active"
    billing_cycle: Optional[str] = None
    next_billing_date: Optional[str] = None
    amount: Optional[float] = None
