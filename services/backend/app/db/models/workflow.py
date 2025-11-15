"""Workflow models"""

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, ForeignKey, Index, Integer, Numeric, String, Text, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class WorkflowFolder(Base, TimestampMixin):
    """Workflow folder for organization"""

    __tablename__ = "workflow_folder"
    __table_args__ = (
        Index("workflow_folder_user_idx", "user_id"),
        Index("workflow_folder_workspace_parent_idx", "workspace_id", "parent_id"),
        Index("workflow_folder_parent_sort_idx", "parent_id", "sort_order"),
    )

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    color: Mapped[str] = mapped_column(Text, nullable=False, default="#6B7280")
    is_expanded: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    user_id: Mapped[str] = mapped_column(
        Text, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    workspace_id: Mapped[str] = mapped_column(
        Text, ForeignKey("workspace.id", ondelete="CASCADE"), nullable=False
    )
    parent_id: Mapped[Optional[str]] = mapped_column(
        Text, ForeignKey("workflow_folder.id", ondelete="CASCADE"), nullable=True
    )

    # Relationships
    user: Mapped["User"] = relationship("User")
    workspace: Mapped["Workspace"] = relationship("Workspace")
    workflows: Mapped[list["Workflow"]] = relationship(
        "Workflow", back_populates="folder", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<WorkflowFolder(id={self.id}, name={self.name})>"


class Workflow(Base, TimestampMixin):
    """Workflow model"""

    __tablename__ = "workflow"
    __table_args__ = (
        Index("workflow_user_id_idx", "user_id"),
        Index("workflow_workspace_id_idx", "workspace_id"),
        Index("workflow_user_workspace_idx", "user_id", "workspace_id"),
        Index("workflow_organization_id_idx", "organization_id"),
    )

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    color: Mapped[str] = mapped_column(Text, nullable=False, default="#3972F6")
    last_synced: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_deployed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    deployed_state: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    deployed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    collaborators: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    run_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_run_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    variables: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    is_published: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    marketplace_data: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    user_id: Mapped[str] = mapped_column(
        Text, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    organization_id: Mapped[Optional[str]] = mapped_column(
        Text, ForeignKey("organization.id", ondelete="SET NULL"), nullable=True
    )
    workspace_id: Mapped[Optional[str]] = mapped_column(
        Text, ForeignKey("workspace.id", ondelete="CASCADE"), nullable=True
    )
    folder_id: Mapped[Optional[str]] = mapped_column(
        Text, ForeignKey("workflow_folder.id", ondelete="SET NULL"), nullable=True
    )
    pinned_api_key_id: Mapped[Optional[str]] = mapped_column(
        Text, ForeignKey("api_key.id", ondelete="SET NULL"), nullable=True
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="workflows")
    workspace: Mapped[Optional["Workspace"]] = relationship("Workspace", back_populates="workflows")
    folder: Mapped[Optional["WorkflowFolder"]] = relationship(
        "WorkflowFolder", back_populates="workflows"
    )
    blocks: Mapped[list["WorkflowBlock"]] = relationship(
        "WorkflowBlock", back_populates="workflow", cascade="all, delete-orphan"
    )
    edges: Mapped[list["WorkflowEdge"]] = relationship(
        "WorkflowEdge", back_populates="workflow", cascade="all, delete-orphan"
    )
    subflows: Mapped[list["WorkflowSubflow"]] = relationship(
        "WorkflowSubflow", back_populates="workflow", cascade="all, delete-orphan"
    )
    execution_snapshots: Mapped[list["WorkflowExecutionSnapshot"]] = relationship(
        "WorkflowExecutionSnapshot", back_populates="workflow", cascade="all, delete-orphan"
    )
    execution_logs: Mapped[list["WorkflowExecutionLog"]] = relationship(
        "WorkflowExecutionLog", back_populates="workflow", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Workflow(id={self.id}, name={self.name})>"


class WorkflowBlock(Base, TimestampMixin):
    """Workflow block model"""

    __tablename__ = "workflow_blocks"
    __table_args__ = (
        Index("workflow_blocks_workflow_id_idx", "workflow_id"),
        Index("workflow_blocks_workflow_type_idx", "workflow_id", "type"),
    )

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    type: Mapped[str] = mapped_column(Text, nullable=False)  # agent, api, function, etc.
    name: Mapped[str] = mapped_column(Text, nullable=False)
    position_x: Mapped[float] = mapped_column(Numeric, nullable=False)
    position_y: Mapped[float] = mapped_column(Numeric, nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    horizontal_handles: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_wide: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    advanced_mode: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    trigger_mode: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    height: Mapped[float] = mapped_column(Numeric, nullable=False, default=0)
    sub_blocks: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    outputs: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    data: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    workflow_id: Mapped[str] = mapped_column(
        Text, ForeignKey("workflow.id", ondelete="CASCADE"), nullable=False
    )

    # Relationships
    workflow: Mapped["Workflow"] = relationship("Workflow", back_populates="blocks")

    def __repr__(self) -> str:
        return f"<WorkflowBlock(id={self.id}, type={self.type}, name={self.name})>"


class WorkflowEdge(Base):
    """Workflow edge (connection) model"""

    __tablename__ = "workflow_edges"
    __table_args__ = (
        Index("workflow_edges_workflow_id_idx", "workflow_id"),
        Index("workflow_edges_workflow_source_idx", "workflow_id", "source_block_id"),
        Index("workflow_edges_workflow_target_idx", "workflow_id", "target_block_id"),
    )

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    source_handle: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    target_handle: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default="now()"
    )

    workflow_id: Mapped[str] = mapped_column(
        Text, ForeignKey("workflow.id", ondelete="CASCADE"), nullable=False
    )
    source_block_id: Mapped[str] = mapped_column(
        Text, ForeignKey("workflow_blocks.id", ondelete="CASCADE"), nullable=False
    )
    target_block_id: Mapped[str] = mapped_column(
        Text, ForeignKey("workflow_blocks.id", ondelete="CASCADE"), nullable=False
    )

    # Relationships
    workflow: Mapped["Workflow"] = relationship("Workflow", back_populates="edges")

    def __repr__(self) -> str:
        return f"<WorkflowEdge(id={self.id}, {self.source_block_id} -> {self.target_block_id})>"


class WorkflowSubflow(Base, TimestampMixin):
    """Workflow subflow (loop/parallel) model"""

    __tablename__ = "workflow_subflows"
    __table_args__ = (
        Index("workflow_subflows_workflow_id_idx", "workflow_id"),
        Index("workflow_subflows_workflow_type_idx", "workflow_id", "type"),
    )

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    type: Mapped[str] = mapped_column(Text, nullable=False)  # loop or parallel
    config: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    workflow_id: Mapped[str] = mapped_column(
        Text, ForeignKey("workflow.id", ondelete="CASCADE"), nullable=False
    )

    # Relationships
    workflow: Mapped["Workflow"] = relationship("Workflow", back_populates="subflows")

    def __repr__(self) -> str:
        return f"<WorkflowSubflow(id={self.id}, type={self.type})>"


class WorkflowExecutionSnapshot(Base):
    """Workflow execution snapshot for deployments"""

    __tablename__ = "workflow_execution_snapshots"
    __table_args__ = (
        Index("workflow_snapshots_workflow_id_idx", "workflow_id"),
        Index("workflow_snapshots_hash_idx", "state_hash"),
        Index("workflow_snapshots_workflow_hash_idx", "workflow_id", "state_hash", unique=True),
        Index("workflow_snapshots_created_at_idx", "created_at"),
    )

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    state_hash: Mapped[str] = mapped_column(Text, nullable=False)
    state_data: Mapped[dict] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default="now()"
    )

    workflow_id: Mapped[str] = mapped_column(
        Text, ForeignKey("workflow.id", ondelete="CASCADE"), nullable=False
    )

    # Relationships
    workflow: Mapped["Workflow"] = relationship("Workflow", back_populates="execution_snapshots")
    execution_logs: Mapped[list["WorkflowExecutionLog"]] = relationship(
        "WorkflowExecutionLog", back_populates="state_snapshot"
    )

    def __repr__(self) -> str:
        return f"<WorkflowExecutionSnapshot(id={self.id}, hash={self.state_hash[:8]})>"


class WorkflowExecutionLog(Base):
    """Workflow execution log model"""

    __tablename__ = "workflow_execution_logs"
    __table_args__ = (
        Index("workflow_logs_workflow_id_idx", "workflow_id"),
        Index("workflow_logs_execution_id_idx", "execution_id"),
        Index("workflow_logs_started_at_idx", "started_at"),
        Index("workflow_logs_workflow_started_idx", "workflow_id", "started_at"),
    )

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    execution_id: Mapped[str] = mapped_column(Text, nullable=False)
    level: Mapped[str] = mapped_column(Text, nullable=False)  # info, error, warning
    trigger: Mapped[str] = mapped_column(Text, nullable=False)  # api, webhook, schedule, manual, chat
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    total_duration_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(Text, nullable=False, default="running")  # running, completed, failed
    input_data: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    output_data: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    trace_id: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    block_logs: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)

    workflow_id: Mapped[str] = mapped_column(
        Text, ForeignKey("workflow.id", ondelete="CASCADE"), nullable=False
    )
    state_snapshot_id: Mapped[str] = mapped_column(
        Text, ForeignKey("workflow_execution_snapshots.id"), nullable=False
    )

    # Relationships
    workflow: Mapped["Workflow"] = relationship("Workflow", back_populates="execution_logs")
    state_snapshot: Mapped["WorkflowExecutionSnapshot"] = relationship(
        "WorkflowExecutionSnapshot", back_populates="execution_logs"
    )

    def __repr__(self) -> str:
        return f"<WorkflowExecutionLog(id={self.id}, execution={self.execution_id}, status={self.status})>"
