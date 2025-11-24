"""
Application configuration settings.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""

    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Vehicle Repair Database API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Comprehensive automotive repair and technical information API"

    # Database
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/vehicle_db"
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20

    # Redis Cache
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL: int = 3600  # 1 hour

    # Elasticsearch
    ELASTICSEARCH_URL: str = "http://localhost:9200"
    ELASTICSEARCH_INDEX: str = "vehicle_repairs"

    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8000"]

    # API Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 100

    # External APIs
    NHTSA_API_BASE_URL: str = "https://vpic.nhtsa.dot.gov/api"
    EPA_API_BASE_URL: str = "https://www.fueleconomy.gov/feg"

    # File Storage
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE_MB: int = 10

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
