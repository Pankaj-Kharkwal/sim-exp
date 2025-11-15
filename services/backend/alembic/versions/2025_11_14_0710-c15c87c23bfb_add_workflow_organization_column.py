"""add organization column to workflows

Revision ID: c15c87c23bfb
Revises: b7d8f0fcb6a1
Create Date: 2025-11-14 07:10:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c15c87c23bfb"
down_revision: Union[str, None] = "b7d8f0fcb6a1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("workflow", sa.Column("organization_id", sa.Text(), nullable=True))
    op.create_foreign_key(
        "workflow_organization_id_fkey",
        "workflow",
        "organization",
        ["organization_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_index(
        "workflow_organization_id_idx", "workflow", ["organization_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index("workflow_organization_id_idx", table_name="workflow")
    op.drop_constraint(
        "workflow_organization_id_fkey", "workflow", type_="foreignkey"
    )
    op.drop_column("workflow", "organization_id")
