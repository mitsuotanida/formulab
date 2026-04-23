import hashlib
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


def register_user(db: Session, email: str, name: str, password: str) -> User:
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise ValueError("Email ya registrado")
    user = User(email=email, name=name, password_hash=hash_password(password))
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
