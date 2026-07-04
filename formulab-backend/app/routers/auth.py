from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth import (
    RegisterRequest, LoginRequest, TokenResponse, RefreshRequest,
    ForgotPasswordRequest, ResetPasswordRequest, MessageResponse, UserBasic,
)
from app.services import auth_service
from app.services import email_service

router = APIRouter(prefix="/auth", tags=["auth"])


def _user_basic(user) -> UserBasic:
    return UserBasic(
        id=str(user.id), name=user.name, nickname=user.nickname,
        email=user.email, role=user.role, xp=user.xp, level=user.level,
        streak=user.streak, is_verified=user.is_verified,
    )


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(body: RegisterRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    try:
        user = auth_service.register_user(db, body.email, body.name, body.password, body.nickname)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    # Send verification email in the background (non-blocking)
    background_tasks.add_task(
        email_service.send_verification_email,
        user.email, user.name, user.verification_token,
    )
    _, access_token, refresh_token = auth_service.login_user(db, body.email, body.password)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token, user=_user_basic(user))


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    try:
        user, access_token, refresh_token = auth_service.login_user(db, body.email, body.password)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    return TokenResponse(access_token=access_token, refresh_token=refresh_token, user=_user_basic(user))


@router.post("/refresh", response_model=TokenResponse)
def refresh(body: RefreshRequest, db: Session = Depends(get_db)):
    try:
        access_token, new_refresh = auth_service.refresh_access_token(db, body.refresh_token)
        from jose import jwt as jose_jwt
        from app.config import settings
        import uuid
        from app.models.user import User
        payload = jose_jwt.decode(access_token, settings.secret_key, algorithms=["HS256"])
        user = db.query(User).filter(User.id == uuid.UUID(payload["sub"])).first()
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    return TokenResponse(access_token=access_token, refresh_token=new_refresh, user=_user_basic(user))


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(body: RefreshRequest, db: Session = Depends(get_db)):
    auth_service.logout_user(db, body.refresh_token)


# ── Email verification ──────────────────────────────────────────────────────

@router.get("/verify-email", response_model=MessageResponse)
def verify_email(token: str = Query(...), db: Session = Depends(get_db)):
    try:
        auth_service.verify_email_token(db, token)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return MessageResponse(message="Cuenta verificada exitosamente")


@router.post("/resend-verification", response_model=MessageResponse, status_code=202)
def resend_verification(body: ForgotPasswordRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    result = auth_service.resend_verification_email(db, body.email)
    if result:
        from app.models.user import User
        user = db.query(User).filter(User.email == body.email).first()
        background_tasks.add_task(email_service.send_verification_email, body.email, user.name, result)
    return MessageResponse(message="Si el email está registrado y sin verificar, recibirás un nuevo enlace")


# ── Password reset ──────────────────────────────────────────────────────────

@router.post("/forgot-password", response_model=MessageResponse, status_code=202)
def forgot_password(body: ForgotPasswordRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    result = auth_service.request_password_reset(db, body.email)
    if result:
        token, name = result
        background_tasks.add_task(email_service.send_reset_email, body.email, name, token)
    return MessageResponse(message="Si el email está registrado, recibirás las instrucciones para restablecer tu contraseña")


@router.post("/reset-password", response_model=MessageResponse)
def reset_password(body: ResetPasswordRequest, db: Session = Depends(get_db)):
    try:
        auth_service.reset_password(db, body.token, body.new_password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return MessageResponse(message="Contraseña restablecida exitosamente. Puedes iniciar sesión.")
