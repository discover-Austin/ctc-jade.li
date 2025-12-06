"""
Base database configuration and session management.
"""
from typing import Any, Generator
from sqlalchemy import create_engine, event, exc, text
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import Pool
import uuid
from datetime import datetime
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

# Database URL from settings
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Create engine with proper pooling and error handling
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT,
    pool_recycle=settings.DB_POOL_RECYCLE,  # Recycle connections after 1 hour
    echo=settings.DB_ECHO,  # SQL logging
    connect_args={
        "connect_timeout": 10,
        "options": "-c timezone=utc"
    }
)


@event.listens_for(Pool, "connect")
def set_session_parameters(dbapi_connection, connection_record):
    """Set session parameters on new connections."""
    cursor = dbapi_connection.cursor()
    cursor.execute("SET timezone='UTC'")
    cursor.close()


@event.listens_for(Pool, "checkout")
def receive_checkout(dbapi_connection, connection_record, connection_proxy):
    """Verify connection is alive on checkout."""
    try:
        cursor = dbapi_connection.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
    except exc.OperationalError as e:
        # Connection is stale, raise DisconnectionError to recycle
        logger.warning(f"Stale connection detected: {e}")
        raise exc.DisconnectionError()


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False  # Don't expire objects after commit
)


@as_declarative()
class Base:
    """Base class for all database models."""

    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency for getting database sessions with proper error handling.

    Yields:
        Database session

    Example:
        @app.get("/items")
        def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()  # Commit successful transactions
    except Exception as e:
        db.rollback()  # Rollback on error
        logger.error(f"Database session error: {e}")
        raise
    finally:
        db.close()


async def check_db_connection() -> bool:
    """
    Check database connectivity.

    Returns:
        True if database is reachable, False otherwise
    """
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return True
    except Exception as e:
        logger.error(f"Database connection check failed: {e}")
        return False


def generate_uuid() -> str:
    """Generate a UUID string."""
    return str(uuid.uuid4())


def get_timestamp() -> datetime:
    """Get current timestamp in UTC."""
    return datetime.utcnow()


def init_db():
    """Initialize database connection pool."""
    try:
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connection pool initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        return False


def close_db():
    """Close database connections and dispose engine."""
    try:
        engine.dispose()
        logger.info("Database connections closed successfully")
    except Exception as e:
        logger.error(f"Error closing database connections: {e}")
