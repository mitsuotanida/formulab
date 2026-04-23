import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

RA_LABELS = {
    1: "Definir variables de decisión",
    2: "Formular función objetivo",
    3: "Expresar restricciones",
    4: "Clasificar tipo de modelo",
    5: "Modelar estructuras especiales",
}


class RATrackingOut(BaseModel):
    ra_id: int
    label: str
    attempts: int
    successes: int
    success_rate: float
    last_attempt: Optional[datetime]

    class Config:
        from_attributes = True


class RATrackingListResponse(BaseModel):
    data: List[RATrackingOut]


class ClassRAEntry(BaseModel):
    user_id: uuid.UUID
    name: str
    ra_1: float
    ra_2: float
    ra_3: float
    ra_4: float
    ra_5: float
