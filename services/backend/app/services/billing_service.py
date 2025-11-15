"""Billing and usage summarisation service."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Any

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.db.models import (
    Organization,
    OrganizationMember,
    User,
    Workflow,
    WorkflowExecutionLog,
    Workspace,
)


logger = get_logger(__name__)


def _next_billing_date() -> str:
    """Return ISO string for the first day of next month."""
    today = date.today()
    if today.month == 12:
        next_month = date(today.year + 1, 1, 1)
    else:
        next_month = date(today.year, today.month + 1, 1)
    return next_month.isoformat()


@dataclass
class UsageSnapshot:
    executions: int
    workflows: int
    last_run: datetime | None


class BillingService:
    """Provides aggregated usage metrics for billing views."""

    async def _workflow_usage_for_user(
        self, user: User, db: AsyncSession
    ) -> UsageSnapshot:
        workflow_ids_stmt = select(Workflow.id).where(Workflow.user_id == user.id)

        workflows_count = await db.scalar(
            select(func.count()).select_from(workflow_ids_stmt.subquery())
        )
        workflows_count = workflows_count or 0

        executions_stmt = (
            select(func.count(WorkflowExecutionLog.id))
            .where(WorkflowExecutionLog.workflow_id.in_(workflow_ids_stmt))
            .subquery()
        )
        executions = await db.scalar(select(executions_stmt))
        executions = executions or 0

        last_run_stmt = (
            select(func.max(WorkflowExecutionLog.started_at))
            .where(WorkflowExecutionLog.workflow_id.in_(workflow_ids_stmt))
        )
        last_run = await db.scalar(last_run_stmt)

        return UsageSnapshot(
            executions=int(executions),
            workflows=int(workflows_count),
            last_run=last_run,
        )

    async def get_user_billing(self, user: User, db: AsyncSession) -> dict[str, Any]:
        """Return per-user billing summary."""
        usage = await self._workflow_usage_for_user(user, db)

        credits_used = round(usage.executions * 0.15, 2)
        credits_remaining = max(0.0, 100 - credits_used)

        subscription = {
            "plan": "builder" if usage.workflows < 10 else "scale",
            "status": "active",
            "billingCycle": "monthly",
            "nextBillingDate": _next_billing_date(),
            "amount": 49 if usage.workflows < 10 else 199,
        }

        recommendations: list[str] = []
        if usage.executions == 0:
            recommendations.append("Run your first workflow to unlock analytics.")
        if usage.workflows >= 10:
            recommendations.append("Consider upgrading to Scale for priority execution lanes.")

        return {
            "subscription": subscription,
            "usage": {
                "executions": usage.executions,
                "workflows": usage.workflows,
                "lastRunAt": usage.last_run.isoformat() if usage.last_run else None,
                "creditsUsed": credits_used,
                "creditsRemaining": credits_remaining,
            },
            "limits": {
                "maxWorkflows": 25,
                "maxExecutionsPerDay": 1000,
            },
            "recommendations": recommendations,
        }

    async def get_organization_billing(
        self, *, organization_id: str, user: User, db: AsyncSession
    ) -> dict[str, Any]:
        """Return organization-level billing metrics."""
        organization = await db.scalar(
            select(Organization).where(Organization.id == organization_id)
        )
        if not organization:
            raise ValueError("Organization not found")

        membership = await db.scalar(
            select(OrganizationMember).where(
                OrganizationMember.organization_id == organization_id,
                OrganizationMember.user_id == user.id,
            )
        )
        if not membership:
            raise PermissionError("User is not part of this organization")

        workspace_ids = (
            select(Workspace.id)
            .where(Workspace.organization_id == organization_id)
            .subquery()
        )
        workflows_stmt = (
            select(func.count(Workflow.id))
            .where(Workflow.workspace_id.in_(workspace_ids))
            .subquery()
        )
        workflow_total = await db.scalar(select(workflows_stmt))
        workflow_total = workflow_total or 0

        executions_stmt = (
            select(func.count(WorkflowExecutionLog.id))
            .join(
                Workflow,
                WorkflowExecutionLog.workflow_id == Workflow.id,
            )
            .where(Workflow.workspace_id.in_(workspace_ids))
        )
        executions_total = await db.scalar(executions_stmt)
        executions_total = executions_total or 0

        member_count = await db.scalar(
            select(func.count(OrganizationMember.id)).where(
                OrganizationMember.organization_id == organization_id
            )
        )
        member_count = member_count or 0

        return {
            "organization": {
                "id": organization.id,
                "name": organization.name,
                "members": member_count,
            },
            "subscription": {
                "plan": "enterprise" if member_count > 20 else "team",
                "status": "active",
                "billingCycle": "annual" if member_count > 20 else "monthly",
                "nextBillingDate": _next_billing_date(),
                "amount": 999 if member_count > 20 else 299,
            },
            "usage": {
                "executions": executions_total,
                "workflows": workflow_total,
                "storageGb": round(workflow_total * 0.35, 2),
                "creditsUsed": round(executions_total * 0.12, 2),
            },
            "limits": {
                "maxSeats": 50 if member_count > 20 else 20,
                "maxWorkflows": 200,
            },
            "recommendations": [
                "Invite teammates to collaborate on shared workspaces.",
                "Set up usage alerts in the Billing tab.",
            ],
        }


billing_service = BillingService()
