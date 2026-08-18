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


def _has_column(table: str, column: str) -> bool:
    bind = op.get_bind()
    insp = sa.inspect(bind)
    return column in {c["name"] for c in insp.get_columns(table)}


def upgrade() -> None:
    # Existing users are marked as verified so they are not locked out.
    # New users registered after this migration start as unverified (default=false via ORM).
    # Each add is guarded so a partially-migrated DB (e.g. created via create_all or a
    # previous deploy) doesn't fail with "column already exists".
    if not _has_column('users', 'is_verified'):
        op.add_column('users', sa.Column('is_verified', sa.Boolean(), nullable=False, server_default='true'))
    if not _has_column('users', 'verification_token'):
        op.add_column('users', sa.Column('verification_token', sa.String(100), nullable=True))
    if not _has_column('users', 'verification_token_expires'):
        op.add_column('users', sa.Column('verification_token_expires', sa.DateTime(timezone=True), nullable=True))
    if not _has_column('users', 'reset_token'):
        op.add_column('users', sa.Column('reset_token', sa.String(100), nullable=True))
    if not _has_column('users', 'reset_token_expires'):
        op.add_column('users', sa.Column('reset_token_expires', sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    for col in ('is_verified', 'verification_token', 'verification_token_expires',
                'reset_token', 'reset_token_expires'):
        if _has_column('users', col):
            op.drop_column('users', col)
