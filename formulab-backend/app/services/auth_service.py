import hashlib
import secrets
import uuid
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.config import settings
from app.models.user import User, RefreshToken
from app.utils.security import hash_password, verify_password

ALGORITHM = "HS256"


def create_access_token(user_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode({"sub": user_id, "exp": expire, "type": "access"}, settings.secret_key, algorithm=ALGORITHM)


def create_refresh_token(user_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)
    return jwt.encode({"sub": user_id, "exp": expire, "type": "refresh"}, settings.refresh_secret_key, algorithm=ALGORITHM)


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def register_user(db: Session, email: str, name: str, password: str, nickname: str | None = None) -> User:
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise ValueError("Email ya registrado")
    token = secrets.token_urlsafe(32)
    expires = datetime.now(timezone.utc) + timedelta(hours=24)
    user = User(
        email=email,
        name=name,
        password_hash=hash_password(password),
        nickname=nickname or None,
        is_verified=False,
        verification_token=token,
        verification_token_expires=expires,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        raise ValueError("Credenciales inválidas")

    access_token = create_access_token(str(user.id))
    refresh_token = create_refresh_token(str(user.id))

    expire = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)
    db.add(RefreshToken(user_id=user.id, token_hash=_hash_token(refresh_token), expires_at=expire))
    db.commit()

    return user, access_token, refresh_token


def refresh_access_token(db: Session, refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, settings.refresh_secret_key, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise ValueError("Token inválido")
        user_id = payload["sub"]
    except JWTError:
        raise ValueError("Token inválido o expirado")

    token_hash = _hash_token(refresh_token)
    stored = db.query(RefreshToken).filter(
        RefreshToken.token_hash == token_hash,
        RefreshToken.revoked == False,
        RefreshToken.expires_at > datetime.now(timezone.utc),
    ).first()
    if not stored:
        raise ValueError("Token no encontrado o revocado")

    stored.revoked = True
    new_refresh = create_refresh_token(user_id)
    expire = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)
    db.add(RefreshToken(user_id=uuid.UUID(user_id), token_hash=_hash_token(new_refresh), expires_at=expire))
    db.commit()

    return create_access_token(user_id), new_refresh


def logout_user(db: Session, refresh_token: str) -> None:
    token_hash = _hash_token(refresh_token)
    stored = db.query(RefreshToken).filter(RefreshToken.token_hash == token_hash).first()
    if stored:
        stored.revoked = True
        db.commit()


def get_current_user(db: Session, token: str) -> User:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        if payload.get("type") != "access":
            raise ValueError("Token inválido")
        user_id = payload["sub"]
    except JWTError:
        raise ValueError("Token inválido o expirado")

    user = db.query(User).filter(User.id == uuid.UUID(user_id)).first()
    if not user:
        raise ValueError("Usuario no encontrado")
    return user


def verify_email_token(db: Session, token: str) -> User:
    user = db.query(User).filter(
        User.verification_token == token,
        User.verification_token_expires > datetime.now(timezone.utc),
        User.is_verified == False,
    ).first()
    if not user:
        raise ValueError("El enlace de verificación es inválido o ya expiró")
    user.is_verified = True
    user.verification_token = None
    user.verification_token_expires = None
    db.commit()
    return user


def resend_verification_email(db: Session, email: str) -> str | None:
    user = db.query(User).filter(User.email == email, User.is_verified == False).first()
    if not user:
        return None
    token = secrets.token_urlsafe(32)
    user.verification_token = token
    user.verification_token_expires = datetime.now(timezone.utc) + timedelta(hours=24)
    db.commit()
    return token


def request_password_reset(db: Session, email: str) -> tuple[str, str] | None:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    token = secrets.token_urlsafe(32)
    user.reset_token = token
    user.reset_token_expires = datetime.now(timezone.utc) + timedelta(minutes=15)
    db.commit()
    return token, user.name


def reset_password(db: Session, token: str, new_password: str) -> None:
    user = db.query(User).filter(
        User.reset_token == token,
        User.reset_token_expires > datetime.now(timezone.utc),
    ).first()
    if not user:
        raise ValueError("El enlace de restablecimiento es inválido o ya expiró")
    user.password_hash = hash_password(new_password)
    user.reset_token = None
    user.reset_token_expires = None
    # Revoke all refresh tokens for security
    db.query(RefreshToken).filter(RefreshToken.user_id == user.id).update({"revoked": True})
    db.commit()
