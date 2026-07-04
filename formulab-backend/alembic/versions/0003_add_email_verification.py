"""add email verification fields to users

Revision ID: 0003
Revises: 0002
Create Date: 2026-07-04
"""
from alembic import op
import sqlalchemy as sa

revision = '0003'
down_revision = '0002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Existing users are marked as verified so they are not locked out.
    # New users registered after this migration start as unverified (default=false via ORM).
    op.add_column('users', sa.Column('is_verified', sa.Boolean(), nullable=False, server_default='true'))
    op.add_column('users', sa.Column('verification_token', sa.String(100), nullable=True))
    op.add_column('users', sa.Column('verification_token_expires', sa.DateTime(timezone=True), nullable=True))
    op.add_column('users', sa.Column('reset_token', sa.String(100), nullable=True))
    op.add_column('users', sa.Column('reset_token_expires', sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'is_verified')
    op.drop_column('users', 'verification_token')
    op.drop_column('users', 'verification_token_expires')
    op.drop_column('users', 'reset_token')
    op.drop_column('users', 'reset_token_expires')
