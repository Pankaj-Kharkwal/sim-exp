"""
Application configuration
"""
import json
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API Settings
    PROJECT_NAME: str = "Pankh.AI"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True
    WORKERS: int = 1
    LOG_LEVEL: str = "info"

    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/pankh_ai"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://frontend:5173",
    ]

    # AI Provider Keys
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = True

        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str):
            if field_name == "CORS_ORIGINS":
                try:
                    return json.loads(raw_val)
                except json.JSONDecodeError:
                    return [raw_val]
            return raw_val


settings = Settings()
