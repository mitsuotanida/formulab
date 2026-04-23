"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-04-20
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Definir ENUMs una sola vez — SQLAlchemy los crea al primer CREATE TABLE que los use
user_role = sa.Enum("student", "teacher", name="user_role")
exercise_type = sa.Enum("LP", "MIP", "NLP", name="exercise_type")
exercise_difficulty = sa.Enum("easy", "medium", "hard", name="exercise_difficulty")
exercise_domain = sa.Enum(
    "production", "logistics", "agriculture", "finance",
    "inventory", "energy", "generic", name="exercise_domain"
)
badge_condition_type = sa.Enum(
    "first_submission", "streak_days", "exercises_completed",
    "score_threshold", "type_mastery", "xp_milestone",
    name="badge_condition_type"
)


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("email", sa.String(255), unique=True, nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("role", user_role, nullable=False, server_default="student"),
        sa.Column("xp", sa.Integer, nullable=False, server_default="0"),
        sa.Column("level", sa.Integer, nullable=False, server_default="1"),
        sa.Column("streak", sa.Integer, nullable=False, server_default="0"),
        sa.Column("last_active_date", sa.Date, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
    )

    op.create_table(
        "refresh_tokens",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("token_hash", sa.String(255), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
    )

    op.create_table(
        "exercises",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("data_table", postgresql.JSONB, nullable=True),
        sa.Column("domain", exercise_domain, nullable=False),
        sa.Column("type", exercise_type, nullable=False),
        sa.Column("difficulty", exercise_difficulty, nullable=False),
        sa.Column("ra_ids", postgresql.ARRAY(sa.Integer), nullable=False, server_default="{}"),
        sa.Column("ai_generated", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("generation_params", postgresql.JSONB, nullable=True),
        sa.Column("hints", postgresql.JSONB, nullable=False, server_default=sa.text("'[]'")),
        sa.Column("reference_solution", postgresql.JSONB, nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
    )

    op.create_table(
        "submissions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("exercise_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("content_parsed", postgresql.JSONB, nullable=True),
        sa.Column("score", sa.Integer, nullable=True),
        sa.Column("feedback", postgresql.JSONB, nullable=True),
        sa.Column("xp_earned", sa.Integer, nullable=False, server_default="0"),
        sa.Column("hints_used", sa.Integer, nullable=False, server_default="0"),
        sa.Column("time_spent_sec", sa.Integer, nullable=True),
        sa.Column("evaluation_status", sa.String(20), nullable=False, server_default="pending"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
    )

    op.create_table(
        "badges",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(100), unique=True, nullable=False),
        sa.Column("description", sa.String(500), nullable=False),
        sa.Column("icon", sa.String(100), nullable=False),
        sa.Column("condition_type", badge_condition_type, nullable=False),
        sa.Column("condition_value", postgresql.JSONB, nullable=False),
        sa.Column("xp_reward", sa.Integer, nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
    )

    op.create_table(
        "user_badges",
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("badge_id", sa.Integer, sa.ForeignKey("badges.id"), primary_key=True),
        sa.Column("earned_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
    )

    op.create_table(
        "ra_tracking",
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("ra_id", sa.Integer, primary_key=True),
        sa.Column("attempts", sa.Integer, nullable=False, server_default="0"),
        sa.Column("successes", sa.Integer, nullable=False, server_default="0"),
        sa.Column("last_attempt", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("ra_id BETWEEN 1 AND 5", name="ck_ra_id_range"),
    )

    op.create_index("idx_submissions_user_id",     "submissions", ["user_id"])
    op.create_index("idx_submissions_exercise_id", "submissions", ["exercise_id"])
    op.create_index("idx_submissions_created_at",  "submissions", [sa.text("created_at DESC")])
    op.create_index("idx_users_xp",                "users",       [sa.text("xp DESC")])
    op.create_index("idx_ra_tracking_user_id",     "ra_tracking", ["user_id"])


def downgrade() -> None:
    op.drop_index("idx_ra_tracking_user_id")
    op.drop_index("idx_users_xp")
    op.drop_index("idx_submissions_created_at")
    op.drop_index("idx_submissions_exercise_id")
    op.drop_index("idx_submissions_user_id")
    op.drop_table("ra_tracking")
    op.drop_table("user_badges")
    op.drop_table("badges")
    op.drop_table("submissions")
    op.drop_table("exercises")
    op.drop_table("refresh_tokens")
    op.drop_table("users")
    badge_condition_type.drop(op.get_bind())
    exercise_domain.drop(op.get_bind())
    exercise_difficulty.drop(op.get_bind())
    exercise_type.drop(op.get_bind())
    user_role.drop(op.get_bind())
