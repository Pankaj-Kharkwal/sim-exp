"""Initial schema

Revision ID: 001_initial
Revises:
Create Date: 2025-01-10 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create user table
    op.create_table('user',
        sa.Column('id', sa.Text(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('email', sa.Text(), nullable=False),
        sa.Column('email_verified', sa.Boolean(), nullable=False),
        sa.Column('image', sa.Text(), nullable=True),
        sa.Column('stripe_customer_id', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    # Create organization table
    op.create_table('organization',
        sa.Column('id', sa.Text(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('slug', sa.Text(), nullable=False),
        sa.Column('logo', sa.Text(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('metadata', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug')
    )
    op.create_index('organization_slug_idx', 'organization', ['slug'])

    # Create session table
    op.create_table('session',
        sa.Column('id', sa.Text(), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('token', sa.Text(), nullable=False),
        sa.Column('ip_address', sa.Text(), nullable=True),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('user_id', sa.Text(), nullable=False),
        sa.Column('active_organization_id', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['active_organization_id'], ['organization.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('token')
    )
    op.create_index('session_user_id_idx', 'session', ['user_id'])
    op.create_index('session_token_idx', 'session', ['token'])

    # Create account table
    op.create_table('account',
        sa.Column('id', sa.Text(), nullable=False),
        sa.Column('account_id', sa.Text(), nullable=False),
        sa.Column('provider_id', sa.Text(), nullable=False),
        sa.Column('access_token', sa.Text(), nullable=True),
        sa.Column('refresh_token', sa.Text(), nullable=True),
        sa.Column('id_token', sa.Text(), nullable=True),
        sa.Column('access_token_expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('refresh_token_expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('scope', sa.Text(), nullable=True),
        sa.Column('password', sa.Text(), nullable=True),
        sa.Column('user_id', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('account_user_id_idx', 'account', ['user_id'])

    # Create verification table
    op.create_table('verification',
        sa.Column('id', sa.Text(), nullable=False),
        sa.Column('identifier', sa.Text(), nullable=False),
        sa.Column('value', sa.Text(), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('verification_identifier_idx', 'verification', ['identifier'])

    # Create organization_member table
    op.create_table('organization_member',
        sa.Column('id', sa.Text(), nullable=False),
        sa.Column('role', sa.Text(), nullable=False),
        sa.Column('organization_id', sa.Text(), nullable=False),
        sa.Column('user_id', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organization.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('org_member_org_id_idx', 'organization_member', ['organization_id'])
    op.create_index('org_member_user_id_idx', 'organization_member', ['user_id'])

    # Create workspace table
    op.create_table('workspace',
        sa.Column('id', sa.Text(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('color', sa.Text(), nullable=False),
        sa.Column('is_default', sa.Boolean(), nullable=False),
        sa.Column('organization_id', sa.Text(), nullable=False),
        sa.Column('owner_id', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organization.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('workspace_org_id_idx', 'workspace', ['organization_id'])
    op.create_index('workspace_owner_id_idx', 'workspace', ['owner_id'])

    # Create api_key table
    op.create_table('api_key',
        sa.Column('id', sa.Text(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('key_hash', sa.Text(), nullable=False),
        sa.Column('key_prefix', sa.Text(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('last_used_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('user_id', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('key_hash')
    )
    op.create_index('api_key_user_id_idx', 'api_key', ['user_id'])
    op.create_index('api_key_key_hash_idx', 'api_key', ['key_hash'])

    # Create workflow_folder table
    op.create_table('workflow_folder',
        sa.Column('id', sa.Text(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('color', sa.Text(), nullable=False),
        sa.Column('is_expanded', sa.Boolean(), nullable=False),
        sa.Column('sort_order', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Text(), nullable=False),
        sa.Column('workspace_id', sa.Text(), nullable=False),
        sa.Column('parent_id', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['workspace_id'], ['workspace.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['parent_id'], ['workflow_folder.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('workflow_folder_user_idx', 'workflow_folder', ['user_id'])
    op.create_index('workflow_folder_workspace_parent_idx', 'workflow_folder', ['workspace_id', 'parent_id'])
    op.create_index('workflow_folder_parent_sort_idx', 'workflow_folder', ['parent_id', 'sort_order'])

    # Create workflow table
    op.create_table('workflow',
        sa.Column('id', sa.Text(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('color', sa.Text(), nullable=False),
        sa.Column('last_synced', sa.DateTime(timezone=True), nullable=False),
        sa.Column('is_deployed', sa.Boolean(), nullable=False),
        sa.Column('deployed_state', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('deployed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('collaborators', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('run_count', sa.Integer(), nullable=False),
        sa.Column('last_run_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('variables', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('is_published', sa.Boolean(), nullable=False),
        sa.Column('marketplace_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('user_id', sa.Text(), nullable=False),
        sa.Column('workspace_id', sa.Text(), nullable=True),
        sa.Column('folder_id', sa.Text(), nullable=True),
        sa.Column('pinned_api_key_id', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['workspace_id'], ['workspace.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['folder_id'], ['workflow_folder.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['pinned_api_key_id'], ['api_key.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('workflow_user_id_idx', 'workflow', ['user_id'])
    op.create_index('workflow_workspace_id_idx', 'workflow', ['workspace_id'])
    op.create_index('workflow_user_workspace_idx', 'workflow', ['user_id', 'workspace_id'])

    # Create workflow_blocks table
    op.create_table('workflow_blocks',
        sa.Column('id', sa.Text(), nullable=False),
        sa.Column('type', sa.Text(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('position_x', sa.Numeric(), nullable=False),
        sa.Column('position_y', sa.Numeric(), nullable=False),
        sa.Column('enabled', sa.Boolean(), nullable=False),
        sa.Column('horizontal_handles', sa.Boolean(), nullable=False),
        sa.Column('is_wide', sa.Boolean(), nullable=False),
        sa.Column('advanced_mode', sa.Boolean(), nullable=False),
        sa.Column('trigger_mode', sa.Boolean(), nullable=False),
        sa.Column('height', sa.Numeric(), nullable=False),
        sa.Column('sub_blocks', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('outputs', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('data', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('workflow_id', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['workflow_id'], ['workflow.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('workflow_blocks_workflow_id_idx', 'workflow_blocks', ['workflow_id'])
    op.create_index('workflow_blocks_workflow_type_idx', 'workflow_blocks', ['workflow_id', 'type'])

    # Create workflow_edges table
    op.create_table('workflow_edges',
        sa.Column('id', sa.Text(), nullable=False),
        sa.Column('source_handle', sa.Text(), nullable=True),
        sa.Column('target_handle', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('workflow_id', sa.Text(), nullable=False),
        sa.Column('source_block_id', sa.Text(), nullable=False),
        sa.Column('target_block_id', sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(['workflow_id'], ['workflow.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['source_block_id'], ['workflow_blocks.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['target_block_id'], ['workflow_blocks.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('workflow_edges_workflow_id_idx', 'workflow_edges', ['workflow_id'])
    op.create_index('workflow_edges_workflow_source_idx', 'workflow_edges', ['workflow_id', 'source_block_id'])
    op.create_index('workflow_edges_workflow_target_idx', 'workflow_edges', ['workflow_id', 'target_block_id'])

    # Create workflow_subflows table
    op.create_table('workflow_subflows',
        sa.Column('id', sa.Text(), nullable=False),
        sa.Column('type', sa.Text(), nullable=False),
        sa.Column('config', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('workflow_id', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['workflow_id'], ['workflow.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('workflow_subflows_workflow_id_idx', 'workflow_subflows', ['workflow_id'])
    op.create_index('workflow_subflows_workflow_type_idx', 'workflow_subflows', ['workflow_id', 'type'])

    # Create workflow_execution_snapshots table
    op.create_table('workflow_execution_snapshots',
        sa.Column('id', sa.Text(), nullable=False),
        sa.Column('state_hash', sa.Text(), nullable=False),
        sa.Column('state_data', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('workflow_id', sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(['workflow_id'], ['workflow.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('workflow_snapshots_workflow_id_idx', 'workflow_execution_snapshots', ['workflow_id'])
    op.create_index('workflow_snapshots_hash_idx', 'workflow_execution_snapshots', ['state_hash'])
    op.create_index('workflow_snapshots_workflow_hash_idx', 'workflow_execution_snapshots', ['workflow_id', 'state_hash'], unique=True)
    op.create_index('workflow_snapshots_created_at_idx', 'workflow_execution_snapshots', ['created_at'])

    # Create workflow_execution_logs table
    op.create_table('workflow_execution_logs',
        sa.Column('id', sa.Text(), nullable=False),
        sa.Column('execution_id', sa.Text(), nullable=False),
        sa.Column('level', sa.Text(), nullable=False),
        sa.Column('trigger', sa.Text(), nullable=False),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('ended_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('total_duration_ms', sa.Integer(), nullable=True),
        sa.Column('status', sa.Text(), nullable=False),
        sa.Column('input_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('output_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('trace_id', sa.Text(), nullable=True),
        sa.Column('block_logs', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('workflow_id', sa.Text(), nullable=False),
        sa.Column('state_snapshot_id', sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(['workflow_id'], ['workflow.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['state_snapshot_id'], ['workflow_execution_snapshots.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('workflow_logs_workflow_id_idx', 'workflow_execution_logs', ['workflow_id'])
    op.create_index('workflow_logs_execution_id_idx', 'workflow_execution_logs', ['execution_id'])
    op.create_index('workflow_logs_started_at_idx', 'workflow_execution_logs', ['started_at'])
    op.create_index('workflow_logs_workflow_started_idx', 'workflow_execution_logs', ['workflow_id', 'started_at'])


def downgrade() -> None:
    op.drop_table('workflow_execution_logs')
    op.drop_table('workflow_execution_snapshots')
    op.drop_table('workflow_subflows')
    op.drop_table('workflow_edges')
    op.drop_table('workflow_blocks')
    op.drop_table('workflow')
    op.drop_table('workflow_folder')
    op.drop_table('api_key')
    op.drop_table('workspace')
    op.drop_table('organization_member')
    op.drop_table('verification')
    op.drop_table('account')
    op.drop_table('session')
    op.drop_table('organization')
    op.drop_table('user')
