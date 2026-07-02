from typing import Optional
from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    email: EmailStr
    name: str
    password: str
    nickname: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: "UserBasic"


class RefreshRequest(BaseModel):
    refresh_token: str


class UserBasic(BaseModel):
    id: str
    name: str
    nickname: Optional[str] = None
    email: str
    role: str
    xp: int
    level: int
    streak: int

    class Config:
        from_attributes = True


TokenResponse.model_rebuild()
