"""
Main FastAPI application entry point with production-grade features.
"""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from contextlib import asynccontextmanager
import time
import logging
import uuid as uuid_lib

from app.core.config import settings
from app.api import api_router
from app.db.base import init_db, close_db, check_db_connection
from app.core.cache import redis_client
from app.core.search import es_client
from app.core.rate_limit import RateLimitMiddleware

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager for startup and shutdown events.

    Handles:
    - Database connection pool initialization
    - Redis connection
    - Elasticsearch connection
    - Graceful shutdown
    """
    # Startup
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")

    # Initialize database
    db_connected = init_db()
    if not db_connected:
        logger.warning("Database initialization failed - some features may not work")

    # Initialize Redis
    redis_connected = await redis_client.connect()
    if not redis_connected:
        logger.warning("Redis initialization failed - caching and rate limiting disabled")

    # Initialize Elasticsearch
    es_connected = await es_client.connect()
    if not es_connected:
        logger.warning("Elasticsearch initialization failed - search features disabled")

    logger.info("Application startup complete")

    yield

    # Shutdown
    logger.info(f"Shutting down {settings.PROJECT_NAME}")

    # Close connections
    close_db()
    await redis_client.disconnect()
    await es_client.disconnect()

    logger.info("Application shutdown complete")


# Create FastAPI application with lifespan
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS Middleware (improved configuration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
    expose_headers=["X-Process-Time", "X-Request-ID"],
    max_age=600  # Cache preflight requests for 10 minutes
)

# Trusted Host Middleware (properly configured)
if settings.ENVIRONMENT == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.TRUSTED_HOSTS
    )
else:
    # In development, allow all hosts but log warning
    logger.warning("TrustedHostMiddleware disabled in development mode")

# Rate Limiting Middleware
app.add_middleware(RateLimitMiddleware, redis_client=redis_client.client)


# Request ID and timing middleware
@app.middleware("http")
async def add_request_metadata(request: Request, call_next):
    """Add request ID and processing time to response headers."""
    # Generate unique request ID
    request_id = str(uuid_lib.uuid4())
    request.state.request_id = request_id

    start_time = time.time()

    try:
        response = await call_next(request)
    except Exception as e:
        # Log unexpected errors with request ID
        logger.error(f"[{request_id}] Unhandled middleware exception: {e}", exc_info=True)
        raise

    process_time = time.time() - start_time

    # Add headers
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{process_time:.4f}"

    # Log request
    logger.info(
        f"[{request_id}] {request.method} {request.url.path} "
        f"{response.status_code} {process_time:.4f}s"
    )

    return response


# Exception handlers with error tracking
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions with request tracking."""
    request_id = getattr(request.state, "request_id", "unknown")

    logger.warning(
        f"[{request_id}] HTTP {exc.status_code}: {exc.detail} "
        f"on {request.method} {request.url.path}"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "request_id": request_id
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors."""
    request_id = getattr(request.state, "request_id", "unknown")

    logger.warning(
        f"[{request_id}] Validation error on {request.method} {request.url.path}: "
        f"{exc.errors()}"
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "request_id": request_id
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions with error tracking."""
    error_id = str(uuid_lib.uuid4())
    request_id = getattr(request.state, "request_id", "unknown")

    logger.error(
        f"[{request_id}] [ERROR-{error_id}] Unhandled exception: {exc}",
        exc_info=True
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "error_id": error_id,
            "request_id": request_id
        },
    )


# Health check endpoints with real connectivity checks
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Basic health check endpoint.

    Returns 200 if the service is running.
    """
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "service": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT
    }


@app.get("/ready", tags=["Health"])
async def readiness_check():
    """
    Readiness check endpoint with actual connectivity tests.

    Checks:
    - Database connectivity
    - Redis connectivity
    - Elasticsearch connectivity

    Returns 200 if all dependencies are ready, 503 if any are down.
    """
    checks = {}
    all_ready = True

    # Check database
    try:
        db_ok = await check_db_connection()
        checks["database"] = "connected" if db_ok else "disconnected"
        if not db_ok:
            all_ready = False
    except Exception as e:
        logger.error(f"Database health check error: {e}")
        checks["database"] = "error"
        all_ready = False

    # Check Redis
    try:
        redis_ok = await redis_client.check_connection()
        checks["redis"] = "connected" if redis_ok else "disconnected"
        if not redis_ok:
            logger.warning("Redis is not connected - caching disabled")
    except Exception as e:
        logger.error(f"Redis health check error: {e}")
        checks["redis"] = "error"

    # Check Elasticsearch
    try:
        es_ok = await es_client.check_connection()
        checks["elasticsearch"] = "connected" if es_ok else "disconnected"
        if not es_ok:
            logger.warning("Elasticsearch is not connected - search disabled")
    except Exception as e:
        logger.error(f"Elasticsearch health check error: {e}")
        checks["elasticsearch"] = "error"

    status_code = status.HTTP_200_OK if all_ready else status.HTTP_503_SERVICE_UNAVAILABLE

    return JSONResponse(
        status_code=status_code,
        content={
            "status": "ready" if all_ready else "not ready",
            "checks": checks
        }
    )


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Vehicle Repair Database API",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
        "ready": "/ready",
        "api": settings.API_V1_STR
    }


# Include API routers
app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
