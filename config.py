from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ENCRYPTION_KEY: str = "dev-encryption-key-change-this-32b"
    DATABASE_URL: str = "sqlite:///./briefcase.db"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    
    class Config:
        env_file = ".env"


settings = Settings()

