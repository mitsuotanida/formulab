from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings


def _normalize_db_url(url: str) -> str:
    """Force the synchronous psycopg2 driver regardless of how the URL is written.

    Managed Postgres providers (Neon, Heroku, etc.) hand out connection strings in
    several schemes. This app uses sync SQLAlchemy + psycopg2, so rewrite any async
    or legacy scheme to the plain `postgresql://` form that defaults to psycopg2.
    """
    if url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://"):]
    if url.startswith("postgresql+asyncpg://"):
        url = "postgresql://" + url[len("postgresql+asyncpg://"):]
    return url


engine = create_engine(_normalize_db_url(settings.database_url), pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
