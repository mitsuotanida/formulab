from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    email: EmailStr
    name: str
    password: str


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
    email: str
    role: str
    xp: int
    level: int
    streak: int

    class Config:
        from_attributes = True


TokenResponse.model_rebuild()
