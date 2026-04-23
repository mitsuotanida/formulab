import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel


class SubmissionCreate(BaseModel):
    exercise_id: uuid.UUID
    content: str
    time_spent_sec: Optional[int] = None
    hints_used: int = 0


class FeedbackComponent(BaseModel):
    score: int
    max: int
    comment: str


class SubmissionFeedback(BaseModel):
    overall: str
    variables: FeedbackComponent
    objective: FeedbackComponent
    constraints: FeedbackComponent
    classification: FeedbackComponent
    hints: List[str] = []


class BadgeEarned(BaseModel):
    id: int
    name: str
    icon: str


class SubmissionOut(BaseModel):
    id: uuid.UUID
    exercise_id: uuid.UUID
    score: Optional[int]
    xp_earned: int
    hints_used: int
    evaluation_status: str
    feedback: Optional[SubmissionFeedback] = None
    badges_earned: List[BadgeEarned] = []
    level_up: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class SubmissionPending(BaseModel):
    submission_id: uuid.UUID
    status: str
    poll_url: str
