import uuid
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, EmailStr


class BadgeOut(BaseModel):
    id: int
    name: str
    description: str
    icon: str

    class Config:
        from_attributes = True


class UserOut(BaseModel):
    id: uuid.UUID
    email: str
    name: str
    nickname: Optional[str] = None
    role: str
    xp: int
    level: int
    streak: int
    last_active_date: Optional[date]
    created_at: datetime
    badges: List[BadgeOut] = []

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    nickname: Optional[str] = None
    password: Optional[str] = None


class LeaderboardEntry(BaseModel):
    rank: int
    user_id: uuid.UUID
    name: str
    nickname: Optional[str] = None
    xp: int
    level: int
    level_name: str
    streak: int
    exercises_completed: int

    class Config:
        from_attributes = True


class LeaderboardResponse(BaseModel):
    data: List[LeaderboardEntry]
    total: int
    page: int
    per_page: int


class ProgressStats(BaseModel):
    user_xp: int
    user_percentile: int
    count: int
    min: float
    q1: float
    median: float
    q3: float
    max: float
    mean: float
