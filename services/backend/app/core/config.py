"""Configuration settings for Pankh.AI Backend"""

from typing import Any, Optional
from pydantic import Field, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Pankh.AI Backend"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "AI-powered workflow orchestration platform"

    # Server
    ENVIRONMENT: str = "production"  # production, development, staging
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4
    RELOAD: bool = False
    DEBUG: bool = False

    @field_validator("DEBUG", mode="before")
    @classmethod
    def validate_debug(cls, v: Any) -> bool:
        """Convert DEBUG string to bool"""
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            return v.lower() in ("true", "1", "yes")
        return bool(v)

    # Security
    SECRET_KEY: str = Field(..., description="Secret key for JWT encoding")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    ENCRYPTION_KEY: str = Field(..., description="Encryption key for sensitive data")

    # Database
    DATABASE_URL: str = Field(..., description="PostgreSQL connection URL")
    DB_ECHO: bool = False
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def validate_database_url(cls, v: Optional[str]) -> str:
        if isinstance(v, str):
            # Handle postgresql:// to postgresql+asyncpg://
            if v.startswith("postgresql://") and "asyncpg" not in v:
                v = v.replace("postgresql://", "postgresql+asyncpg://", 1)
        return str(v)

    # Redis
    REDIS_URL: Optional[str] = Field(None, description="Redis connection URL")
    REDIS_PREFIX: str = "pankh:"

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:3001"],
        description="Allowed CORS origins",
    )

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Any) -> list[str]:
        """Parse CORS origins from env (JSON string or comma-separated)"""
        import json
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            # Debug logging
            print(f"DEBUG: Raw CORS value length: {len(v)}, value: {v[:200]}")
            try:
                # Try parsing as JSON array
                result = json.loads(v)
                print(f"DEBUG: Parsed {len(result)} origins: {result}")
                return result
            except json.JSONDecodeError as e:
                print(f"DEBUG: JSON parse error: {e}")
                # Fall back to comma-separated
                return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    FRONTEND_URL: str = Field(
        default="http://localhost:5173",
        description="Frontend application URL"
    )

    # AI Providers
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None

    # Azure OpenAI
    AZURE_OPENAI_ENDPOINT: Optional[str] = None
    AZURE_OPENAI_API_KEY: Optional[str] = None
    AZURE_OPENAI_API_VERSION: str = "2024-12-01-preview"
    AZURE_OPENAI_DEPLOYMENT_CHAT: str = "gpt-5-mini"
    AZURE_OPENAI_DEPLOYMENT_CODE: str = "gpt-5-mini"
    AZURE_OPENAI_DEPLOYMENT_EMBEDDINGS: str = "text-embedding-3-large"

    # Storage
    STORAGE_TYPE: str = "local"  # local, azure, s3
    LOCAL_STORAGE_PATH: str = "./storage"
    AZURE_STORAGE_CONNECTION_STRING: Optional[str] = None
    AZURE_STORAGE_ACCOUNT_URL: Optional[str] = None
    AZURE_STORAGE_ACCOUNT_NAME: Optional[str] = None
    AZURE_STORAGE_ACCOUNT_KEY: Optional[str] = None
    AZURE_STORAGE_CONTAINER: str = "workflows"
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_S3_BUCKET: Optional[str] = None
    AWS_REGION: str = "us-east-1"

    # Email
    RESEND_API_KEY: Optional[str] = None
    FROM_EMAIL: str = "noreply@pankh.ai"

    # Celery
    CELERY_BROKER_URL: Optional[str] = Field(None, description="Celery broker URL")
    CELERY_RESULT_BACKEND: Optional[str] = Field(None, description="Celery result backend")

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"  # json or console

    # Azure Application Insights
    APPLICATIONINSIGHTS_CONNECTION_STRING: Optional[str] = None

    # Feature Flags
    ENABLE_BLOCK_GENERATION: bool = True
    ENABLE_COPILOT: bool = True
    ENABLE_TELEMETRY: bool = True

    # Execution
    MAX_EXECUTION_TIME: int = 600  # seconds
    MAX_PARALLEL_EXECUTIONS: int = 10


# Global settings instance
settings = Settings()
