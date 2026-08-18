"""add nickname to users

Revision ID: 0002
Revises: 0001
Create Date: 2026-07-01
"""
from alembic import op
import sqlalchemy as sa

revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None


def _has_column(table: str, column: str) -> bool:
    bind = op.get_bind()
    insp = sa.inspect(bind)
    return column in {c["name"] for c in insp.get_columns(table)}


def upgrade() -> None:
    # Defensive: the column may already exist if the DB was created outside Alembic
    # (e.g. an earlier create_all() or a previous deploy). Skip if present.
    if not _has_column('users', 'nickname'):
        op.add_column('users', sa.Column('nickname', sa.String(50), nullable=True))


def downgrade() -> None:
    if _has_column('users', 'nickname'):
        op.drop_column('users', 'nickname')
