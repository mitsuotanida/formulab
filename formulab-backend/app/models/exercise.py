import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY, INTEGER
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SAEnum
from app.database import Base


class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    data_table: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    domain: Mapped[str] = mapped_column(
        SAEnum("production", "logistics", "agriculture", "finance", "inventory", "energy", "generic", name="exercise_domain"),
        nullable=False
    )
    type: Mapped[str] = mapped_column(
        SAEnum("LP", "MIP", "NLP", name="exercise_type"),
        nullable=False
    )
    difficulty: Mapped[str] = mapped_column(
        SAEnum("easy", "medium", "hard", name="exercise_difficulty"),
        nullable=False
    )
    ra_ids: Mapped[list] = mapped_column(ARRAY(INTEGER), nullable=False, default=list)
    ai_generated: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    generation_params: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    hints: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    reference_solution: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    submissions = relationship("Submission", back_populates="exercise", cascade="all, delete-orphan")
