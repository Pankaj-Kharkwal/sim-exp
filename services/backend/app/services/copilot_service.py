"""Copilot helper service with rule-based logic."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.db.models import Workflow, WorkflowBlock, WorkflowEdge
from app.services.workflow_service import WorkflowService


logger = get_logger(__name__)


@dataclass
class BlockCatalogEntry:
    """Predefined block metadata used for lightweight suggestions."""

    type: str
    name: str
    description: str
    keywords: tuple[str, ...]
    suggested_data: dict[str, Any]


class CopilotService:
    """Provides workflow suggestions and lightweight analyses without external LLMs."""

    def __init__(self) -> None:
        self._workflow_service = WorkflowService()
        self._catalog: list[BlockCatalogEntry] = [
            BlockCatalogEntry(
                type="http_request",
                name="HTTP Request",
                description="Connects to REST APIs and fetches data.",
                keywords=("api", "http", "request", "webhook"),
                suggested_data={"method": "GET", "url": "https://api.example.com"},
            ),
            BlockCatalogEntry(
                type="send_email",
                name="Send Email",
                description="Delivers transactional or notification emails.",
                keywords=("email", "notify", "notification"),
                suggested_data={"provider": "resend", "subject": "Workflow Notification"},
            ),
            BlockCatalogEntry(
                type="slack_message",
                name="Slack Message",
                description="Posts a formatted message into Slack channels.",
                keywords=("slack", "chatops", "message"),
                suggested_data={"channel": "#automations"},
            ),
            BlockCatalogEntry(
                type="python_function",
                name="Python Function",
                description="Executes custom Python code for data wrangling.",
                keywords=("python", "transform", "script", "code"),
                suggested_data={"runtime": "python3.11", "timeout": 30},
            ),
            BlockCatalogEntry(
                type="decision",
                name="Decision Router",
                description="Branches execution path based on incoming data.",
                keywords=("decision", "branch", "condition"),
                suggested_data={"rules": []},
            ),
        ]

    async def get_suggestions(
        self,
        *,
        prompt: str,
        workflow_id: Optional[str],
        action: str,
        db: AsyncSession,
    ) -> dict[str, Any]:
        """Return structured block suggestions and workflow insights."""
        normalized = prompt.lower()
        scored: list[tuple[int, BlockCatalogEntry]] = []

        for entry in self._catalog:
            score = sum(1 for keyword in entry.keywords if keyword in normalized)
            if score or action == "generate":
                scored.append((score, entry))

        scored.sort(key=lambda item: item[0], reverse=True)
        if not scored:
            scored = [(0, self._catalog[0])]

        suggestions = [
            {
                "type": entry.type,
                "name": entry.name,
                "description": entry.description,
                "suggestedData": entry.suggested_data,
                "confidence": min(0.9, 0.4 + (score * 0.15)),
            }
            for score, entry in scored[:4]
        ]

        workflow_updates: Optional[dict[str, Any]] = None
        if workflow_id:
            workflow_updates = await self._summarize_workflow(workflow_id, db)

        return {
            "suggestions": suggestions,
            "explanation": self._build_explanation(prompt, suggestions, workflow_updates),
            "workflowUpdates": workflow_updates,
        }

    async def _summarize_workflow(
        self, workflow_id: str, db: AsyncSession
    ) -> Optional[dict[str, Any]]:
        workflow = await self._workflow_service.get_workflow(
            workflow_id, db, include_blocks=True, include_edges=True
        )
        if not workflow:
            return None

        trigger_blocks = [b for b in workflow.blocks if b.trigger_mode]
        return {
            "workflowId": workflow_id,
            "name": workflow.name,
            "blockCount": len(workflow.blocks),
            "edgeCount": len(workflow.edges),
            "hasTrigger": bool(trigger_blocks),
            "lastRunAt": workflow.last_run_at.isoformat() if workflow.last_run_at else None,
        }

    def _build_explanation(
        self,
        prompt: str,
        suggestions: list[dict[str, Any]],
        workflow_updates: Optional[dict[str, Any]],
    ) -> str:
        summary = [f"Prompt analysed: {prompt}."]
        summary.append(
            "Top suggestions: "
            + ", ".join(f"{s['name']} ({s['type']})" for s in suggestions)
            + "."
        )
        if workflow_updates:
            summary.append(
                f"Workflow **{workflow_updates['name']}** "
                f"currently contains {workflow_updates['blockCount']} blocks."
            )
            if not workflow_updates.get("hasTrigger"):
                summary.append("Consider adding a trigger block to start executions.")
        return " ".join(summary)

    async def generate_custom_block(
        self,
        *,
        description: str,
        inputs: list[str],
        outputs: list[str],
        language: str,
    ) -> dict[str, Any]:
        """Return deterministic block code."""
        code_lines = [
            f"# Auto-generated block ({language})",
            "def handler(event: dict) -> dict:",
            f"    \"\"\"{description}\"\"\"",
        ]
        if inputs:
            code_lines.append("    # Inputs: " + ", ".join(inputs))
        code_lines.append("    result = {}")
        if outputs:
            code_lines.append("    # TODO: populate outputs")
            for output in outputs:
                code_lines.append(f"    result['{output}'] = event.get('{output}')")
        else:
            code_lines.append("    # No declared outputs; echo input")
            code_lines.append("    result['echo'] = event")
        code_lines.append("    return result")

        return {
            "type": "custom_code",
            "name": f"Generated {language.title()} Block",
            "description": description,
            "code": "\n".join(code_lines),
            "inputs": [{"name": name, "type": "string"} for name in inputs] or [],
            "outputs": [{"name": name, "type": "string"} for name in (outputs or ["echo"])],
            "testCases": [
                {
                    "name": "Smoke test",
                    "input": {name: "value" for name in inputs},
                    "expected": {name: "value" for name in (outputs or ["echo"])},
                }
            ],
        }

    async def explain_workflow(self, workflow_id: str, db: AsyncSession) -> dict[str, Any]:
        """Return textual explanation for a workflow."""
        workflow = await self._workflow_service.get_workflow(
            workflow_id, db, include_blocks=True, include_edges=True
        )
        if not workflow:
            raise ValueError("Workflow not found")

        block_lines = [
            f"- {block.name} ({block.type})"
            for block in sorted(workflow.blocks, key=lambda b: b.position_y)
        ]

        explanation = [
            f"Workflow **{workflow.name}** currently has {len(workflow.blocks)} blocks.",
            "Execution order is determined by the connections between these blocks.",
        ]
        if block_lines:
            explanation.append("Key blocks:\n" + "\n".join(block_lines[:8]))
        if not any(block.trigger_mode for block in workflow.blocks):
            explanation.append("I did not detect an entry trigger block.")

        return {
            "workflowId": workflow_id,
            "summary": " ".join(explanation),
            "generatedAt": datetime.utcnow().isoformat(),
        }

    async def fix_workflow_errors(
        self, workflow_id: str, db: AsyncSession
    ) -> dict[str, Any]:
        """Return diagnostics with lightweight fixes."""
        workflow = await self._workflow_service.get_workflow(
            workflow_id, db, include_blocks=True, include_edges=True
        )
        if not workflow:
            raise ValueError("Workflow not found")

        issues: list[dict[str, Any]] = []
        fixes: list[str] = []

        block_ids = {block.id for block in workflow.blocks}
        if not workflow.blocks:
            issues.append({"code": "missing_blocks", "message": "No blocks configured."})
            fixes.append("Add at least one trigger block and an action block.")

        connected_ids = set()
        for edge in workflow.edges:
            if edge.source_block_id not in block_ids or edge.target_block_id not in block_ids:
                issues.append(
                    {
                        "code": "invalid_edge",
                        "message": f"Edge {edge.id} references missing blocks.",
                    }
                )
                continue
            connected_ids.add(edge.source_block_id)
            connected_ids.add(edge.target_block_id)

        orphan_blocks = [block.name for block in workflow.blocks if block.id not in connected_ids]
        if orphan_blocks:
            issues.append(
                {
                    "code": "orphan_blocks",
                    "message": f"Blocks not connected: {', '.join(orphan_blocks)}",
                }
            )
            fixes.append("Connect orphaned blocks or remove them from the workflow.")

        if not any(block.trigger_mode for block in workflow.blocks):
            issues.append({"code": "missing_trigger", "message": "No trigger block found."})
            fixes.append("Add a Trigger block to start the workflow.")

        status = "healthy" if not issues else "action_required"
        return {
            "workflowId": workflow_id,
            "status": status,
            "issues": issues,
            "suggestedFixes": fixes or ["No changes required."],
        }


copilot_service = CopilotService()
