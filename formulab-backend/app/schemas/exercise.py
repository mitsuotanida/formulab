import uuid
from datetime import datetime
from typing import Optional, List, Any, Dict
from pydantic import BaseModel


class DataTable(BaseModel):
    headers: List[str]
    rows: List[List[str]]


class ExerciseCreate(BaseModel):
    title: str
    description: str
    data_table: Optional[DataTable] = None
    domain: str
    type: str
    difficulty: str
    ra_ids: List[int]
    hints: List[Dict[str, Any]] = []
    reference_solution: Optional[Dict[str, str]] = None


class ExerciseGenerateRequest(BaseModel):
    type: str
    domain: str
    difficulty: str
    ra_focus: List[int] = []
    custom_context: Optional[str] = None


class ExerciseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    data_table: Optional[DataTable] = None
    domain: Optional[str] = None
    type: Optional[str] = None
    difficulty: Optional[str] = None
    ra_ids: Optional[List[int]] = None
    hints: Optional[List[Dict[str, Any]]] = None
    is_active: Optional[bool] = None


class ExerciseOut(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    data_table: Optional[Dict] = None
    domain: str
    type: str
    difficulty: str
    ra_ids: List[int]
    ai_generated: bool
    hints_count: int = 0
    created_at: datetime
    user_best_score: Optional[int] = None
    user_attempts: int = 0

    class Config:
        from_attributes = True


class ExerciseDetail(ExerciseOut):
    hints: List[Dict] = []


class ExerciseListResponse(BaseModel):
    data: List[ExerciseOut]
    total: int
