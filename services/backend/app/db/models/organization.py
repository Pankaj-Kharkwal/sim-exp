"""Organization and workspace models"""

from typing import Optional

from sqlalchemy import Boolean, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class Organization(Base, TimestampMixin):
    """Organization model"""

    __tablename__ = "organization"
    __table_args__ = (Index("organization_slug_idx", "slug"),)

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    slug: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    logo: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    org_metadata: Mapped[Optional[dict]] = mapped_column(type_=Text, nullable=True)

    # Relationships
    members: Mapped[list["OrganizationMember"]] = relationship(
        "OrganizationMember", back_populates="organization", cascade="all, delete-orphan"
    )
    workspaces: Mapped[list["Workspace"]] = relationship(
        "Workspace", back_populates="organization", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Organization(id={self.id}, name={self.name})>"


class OrganizationMember(Base, TimestampMixin):
    """Organization member model"""

    __tablename__ = "organization_member"
    __table_args__ = (
        Index("org_member_org_id_idx", "organization_id"),
        Index("org_member_user_id_idx", "user_id"),
    )

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    role: Mapped[str] = mapped_column(Text, nullable=False, default="member")  # owner, admin, member

    organization_id: Mapped[str] = mapped_column(
        Text, ForeignKey("organization.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[str] = mapped_column(
        Text, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )

    # Relationships
    organization: Mapped["Organization"] = relationship("Organization", back_populates="members")
    user: Mapped["User"] = relationship("User")

    def __repr__(self) -> str:
        return f"<OrganizationMember(org={self.organization_id}, user={self.user_id}, role={self.role})>"


class Workspace(Base, TimestampMixin):
    """Workspace model"""

    __tablename__ = "workspace"
    __table_args__ = (
        Index("workspace_org_id_idx", "organization_id"),
        Index("workspace_owner_id_idx", "owner_id"),
    )

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    color: Mapped[str] = mapped_column(Text, nullable=False, default="#3972F6")
    is_default: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    organization_id: Mapped[str] = mapped_column(
        Text, ForeignKey("organization.id", ondelete="CASCADE"), nullable=False
    )
    owner_id: Mapped[str] = mapped_column(
        Text, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )

    # Relationships
    organization: Mapped["Organization"] = relationship("Organization", back_populates="workspaces")
    owner: Mapped["User"] = relationship("User")
    workflows: Mapped[list["Workflow"]] = relationship(
        "Workflow", back_populates="workspace", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Workspace(id={self.id}, name={self.name})>"
