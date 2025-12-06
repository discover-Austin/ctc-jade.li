"""
Application configuration settings.
"""
from pydantic_settings import BaseSettings
from pydantic import field_validator, ValidationInfo
from typing import List, Optional
import secrets
import os


class Settings(BaseSettings):
    """Application settings."""

    # Environment
    ENVIRONMENT: str = "development"

    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Vehicle Repair Database API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Comprehensive automotive repair and technical information API"

    # Database
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/vehicle_db"
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 3600
    DB_ECHO: bool = False

    # Redis Cache
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_MAX_CONNECTIONS: int = 50
    CACHE_TTL: int = 3600  # 1 hour

    # Elasticsearch
    ELASTICSEARCH_URL: str = "http://localhost:9200"
    ELASTICSEARCH_INDEX: str = "vehicle_repairs"

    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    PASSWORD_MIN_LENGTH: int = 8
    MAX_LOGIN_ATTEMPTS: int = 5
    ACCOUNT_LOCKOUT_MINUTES: int = 15

    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v: str, info: ValidationInfo) -> str:
        """Validate that SECRET_KEY is changed from default in production."""
        # Get environment from values being validated
        environment = info.data.get("ENVIRONMENT", "development")

        if environment == "production" and v == "your-secret-key-change-this-in-production":
            raise ValueError(
                "SECRET_KEY must be changed from default value in production! "
                "Generate one using: python -c 'import secrets; print(secrets.token_urlsafe(32))'"
            )

        if len(v) < 32 and environment == "production":
            raise ValueError("SECRET_KEY must be at least 32 characters in production")

        return v

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    TRUSTED_HOSTS: List[str] = ["localhost", "127.0.0.1"]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v) -> List[str]:
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    @field_validator("TRUSTED_HOSTS", mode="before")
    @classmethod
    def parse_trusted_hosts(cls, v) -> List[str]:
        """Parse trusted hosts from string or list."""
        if isinstance(v, str):
            return [host.strip() for host in v.split(",")]
        return v

    # API Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 100
    RATE_LIMIT_ENABLED: bool = True

    # External APIs
    NHTSA_API_BASE_URL: str = "https://vpic.nhtsa.dot.gov/api"
    NHTSA_API_TIMEOUT: int = 10
    EPA_API_BASE_URL: str = "https://www.fueleconomy.gov/feg"
    EXTERNAL_API_RETRY_ATTEMPTS: int = 3
    EXTERNAL_API_RETRY_DELAY: float = 1.0

    # File Storage
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE_MB: int = 10

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Health Check
    HEALTH_CHECK_TIMEOUT: int = 5

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
