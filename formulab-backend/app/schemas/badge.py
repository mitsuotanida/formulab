from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel


class BadgeOut(BaseModel):
    id: int
    name: str
    description: str
    icon: str
    condition_type: str
    condition_value: Dict[str, Any]
    xp_reward: int
    earned: bool = False
    earned_at: Optional[datetime] = None

    class Config:
        from_attributes = True
