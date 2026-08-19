"""repair schema when users table is partial/legacy

Revision ID: 0004
Revises: 0003
Create Date: 2026-08-18

Some databases ended up with a stub `users` table missing core columns (e.g.
`name`) while alembic_version already pointed at 0003, so earlier migrations
never re-ran to fix it. This migration is new, so `alembic upgrade head` will
execute it once: if the schema is broken it drops the incomplete app tables and
rebuilds the full, correct schema from the ORM models. Healthy databases skip.
"""
from alembic import op
import sqlalchemy as sa

revision = '0004'
down_revision = '0003'
branch_labels = None
depends_on = None

APP_TABLES = ("ra_tracking", "user_badges", "submissions", "refresh_tokens",
              "exercises", "badges", "users")
APP_ENUMS = ("badge_condition_type", "exercise_domain", "exercise_difficulty",
             "exercise_type", "user_role")


def upgrade() -> None:
    bind = op.get_bind()
    insp = sa.inspect(bind)
    has_users = "users" in insp.get_table_names()
    has_name = has_users and "name" in {c["name"] for c in insp.get_columns("users")}
    if has_name:
        # Schema is healthy — nothing to repair.
        return

    # Partial/legacy schema: drop the incomplete app tables and enum types, then
    # recreate the complete schema from the ORM models (the source of truth).
    for t in APP_TABLES:
        op.execute(f'DROP TABLE IF EXISTS "{t}" CASCADE')
    for e in APP_ENUMS:
        op.execute(f"DROP TYPE IF EXISTS {e} CASCADE")

    from app.database import Base
    import app.models  # noqa: F401 — registers all models on Base.metadata
    Base.metadata.create_all(bind)


def downgrade() -> None:
    # One-way repair; nothing to undo.
    pass
