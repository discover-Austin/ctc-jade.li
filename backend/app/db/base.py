"""
Base database configuration and session management.
"""
from typing import Any
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker
import uuid
from datetime import datetime

# Database URL - will be configured via environment variables
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/vehicle_db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@as_declarative()
class Base:
    """Base class for all database models."""

    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


def get_db():
    """Dependency for getting database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def generate_uuid() -> str:
    """Generate a UUID string."""
    return str(uuid.uuid4())


def get_timestamp() -> datetime:
    """Get current timestamp."""
    return datetime.utcnow()
