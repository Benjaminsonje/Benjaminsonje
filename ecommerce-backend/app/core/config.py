from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import field_validator
import secrets


class Settings(BaseSettings):
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./ecommerce.db"
    CORS_ORIGINS: str = "*"

    @field_validator("SQLALCHEMY_DATABASE_URI")
    @classmethod
    def validate_db_uri(cls, v: str) -> str:
        if v.startswith("sqlite"):
            return v
        return v

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()