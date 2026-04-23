from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    database_url: str
    anthropic_api_key: str
    secret_key: str
    refresh_secret_key: str
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 30
    cors_origins: List[str] = ["http://localhost:3000"]
    environment: str = "development"

    class Config:
        env_file = ".env"


settings = Settings()
