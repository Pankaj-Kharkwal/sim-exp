"""add_workflow_templates

Revision ID: a4d990811aa2
Revises: 001_initial
Create Date: 2025-11-14 06:55:52.417832

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4d990811aa2'
down_revision: Union[str, None] = '001_initial'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create workflow_template table
    op.create_table(
        'workflow_template',
        sa.Column('id', sa.Text(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.Text(), nullable=False, server_default='other'),
        sa.Column('icon', sa.Text(), nullable=False, server_default='workflow'),
        sa.Column('color', sa.Text(), nullable=False, server_default='#3972F6'),
        sa.Column('workflow_state', sa.dialects.postgresql.JSONB(), nullable=False),
        sa.Column('views', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('uses', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('is_public', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('author_name', sa.Text(), nullable=False),
        sa.Column('author_avatar', sa.Text(), nullable=True),
        sa.Column('user_id', sa.Text(), nullable=False),
        sa.Column('workspace_id', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['workspace_id'], ['workspace.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes for workflow_template
    op.create_index('template_user_id_idx', 'workflow_template', ['user_id'])
    op.create_index('template_workspace_id_idx', 'workflow_template', ['workspace_id'])
    op.create_index('template_category_idx', 'workflow_template', ['category'])
    op.create_index('template_is_public_idx', 'workflow_template', ['is_public'])
    op.create_index('template_views_idx', 'workflow_template', ['views'])
    op.create_index('template_created_at_idx', 'workflow_template', ['created_at'])

    # Create template_star table
    op.create_table(
        'template_star',
        sa.Column('id', sa.Text(), nullable=False),
        sa.Column('template_id', sa.Text(), nullable=False),
        sa.Column('user_id', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['template_id'], ['workflow_template.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes for template_star
    op.create_index('template_star_template_idx', 'template_star', ['template_id'])
    op.create_index('template_star_user_idx', 'template_star', ['user_id'])
    op.create_index('template_star_unique_idx', 'template_star', ['template_id', 'user_id'], unique=True)


def downgrade() -> None:
    # Drop template_star table and indexes
    op.drop_index('template_star_unique_idx', table_name='template_star')
    op.drop_index('template_star_user_idx', table_name='template_star')
    op.drop_index('template_star_template_idx', table_name='template_star')
    op.drop_table('template_star')

    # Drop workflow_template table and indexes
    op.drop_index('template_created_at_idx', table_name='workflow_template')
    op.drop_index('template_views_idx', table_name='workflow_template')
    op.drop_index('template_is_public_idx', table_name='workflow_template')
    op.drop_index('template_category_idx', table_name='workflow_template')
    op.drop_index('template_workspace_id_idx', table_name='workflow_template')
    op.drop_index('template_user_id_idx', table_name='workflow_template')
    op.drop_table('workflow_template')
