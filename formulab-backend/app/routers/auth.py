from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, RefreshRequest, UserBasic
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(body: RegisterRequest, db: Session = Depends(get_db)):
    try:
        user = auth_service.register_user(db, body.email, body.name, body.password, body.nickname)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    _, access_token, refresh_token = auth_service.login_user(db, body.email, body.password)
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserBasic(id=str(user.id), name=user.name, nickname=user.nickname, email=user.email, role=user.role, xp=user.xp, level=user.level, streak=user.streak),
    )


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    try:
        user, access_token, refresh_token = auth_service.login_user(db, body.email, body.password)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserBasic(id=str(user.id), name=user.name, nickname=user.nickname, email=user.email, role=user.role, xp=user.xp, level=user.level, streak=user.streak),
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh(body: RefreshRequest, db: Session = Depends(get_db)):
    try:
        access_token, new_refresh = auth_service.refresh_access_token(db, body.refresh_token)
        from jose import jwt
        from app.config import settings
        payload = jwt.decode(access_token, settings.secret_key, algorithms=["HS256"])
        from app.models.user import User
        import uuid
        user = db.query(User).filter(User.id == uuid.UUID(payload["sub"])).first()
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    return TokenResponse(
        access_token=access_token,
        refresh_token=new_refresh,
        user=UserBasic(id=str(user.id), name=user.name, nickname=user.nickname, email=user.email, role=user.role, xp=user.xp, level=user.level, streak=user.streak),
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(body: RefreshRequest, db: Session = Depends(get_db)):
    auth_service.logout_user(db, body.refresh_token)
