"""Template models"""

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, ForeignKey, Index, Integer, String, Text, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class WorkflowTemplate(Base, TimestampMixin):
    """Workflow template model for sharing and reusing workflows"""

    __tablename__ = "workflow_template"
    __table_args__ = (
        Index("template_user_id_idx", "user_id"),
        Index("template_workspace_id_idx", "workspace_id"),
        Index("template_category_idx", "category"),
        Index("template_is_public_idx", "is_public"),
        Index("template_views_idx", "views"),
        Index("template_created_at_idx", "created_at"),
    )

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Template metadata
    category: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="other"
    )  # marketing, sales, finance, support, ai, other
    icon: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="workflow"
    )  # lucide icon name
    color: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="#3972F6"
    )  # hex color

    # Workflow state - stores complete workflow configuration
    workflow_state: Mapped[dict] = mapped_column(JSONB, nullable=False)

    # Stats
    views: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    uses: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # Visibility
    is_public: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # Author information
    author_name: Mapped[str] = mapped_column(Text, nullable=False)
    author_avatar: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    user_id: Mapped[str] = mapped_column(
        Text, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    workspace_id: Mapped[str] = mapped_column(
        Text, ForeignKey("workspace.id", ondelete="CASCADE"), nullable=False
    )

    # Relationships
    user: Mapped["User"] = relationship("User")
    workspace: Mapped["Workspace"] = relationship("Workspace")
    stars: Mapped[list["TemplateStar"]] = relationship(
        "TemplateStar", back_populates="template", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<WorkflowTemplate(id={self.id}, name={self.name})>"


class TemplateStar(Base):
    """Template star/favorite model"""

    __tablename__ = "template_star"
    __table_args__ = (
        Index("template_star_template_idx", "template_id"),
        Index("template_star_user_idx", "user_id"),
        # Prevent duplicate stars from same user
        Index("template_star_unique_idx", "template_id", "user_id", unique=True),
    )

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default="now()"
    )

    template_id: Mapped[str] = mapped_column(
        Text, ForeignKey("workflow_template.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[str] = mapped_column(
        Text, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )

    # Relationships
    template: Mapped["WorkflowTemplate"] = relationship("WorkflowTemplate", back_populates="stars")
    user: Mapped["User"] = relationship("User")

    def __repr__(self) -> str:
        return f"<TemplateStar(template_id={self.template_id}, user_id={self.user_id})>"
