"""
Authentication API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Any

from app.db.base import get_db
from app.models.user import User, RefreshToken, UserRole
from app.schemas.auth import (
    UserCreate,
    UserLogin,
    Token,
    UserResponse,
    APIKeyCreate,
    APIKeyResponse,
    PasswordChange,
    TokenRefresh
)
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    generate_api_key,
    hash_api_key,
    get_current_user,
    get_current_active_user
)
from app.core.config import settings

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
) -> Any:
    """
    Register a new user.

    - **email**: Valid email address
    - **username**: Unique username (3-100 characters, alphanumeric)
    - **password**: Strong password (min 8 chars, must include uppercase, lowercase, and digit)
    - **full_name**: Optional full name
    """
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()

    if existing_user:
        if existing_user.email == user_data.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )

    # Create new user
    hashed_password = hash_password(user_data.password)
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        role=UserRole.USER,
        is_active=True,
        is_verified=False
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login", response_model=Token)
async def login(
    credentials: UserLogin,
    db: Session = Depends(get_db)
) -> Any:
    """
    Login with username and password to receive JWT tokens.

    - **username**: Username or email
    - **password**: User password

    Returns:
    - **access_token**: Short-lived JWT token for API access
    - **refresh_token**: Long-lived token for obtaining new access tokens
    - **token_type**: Bearer
    - **expires_in**: Access token expiration time in seconds
    """
    # Find user by username or email
    user = db.query(User).filter(
        (User.username == credentials.username) | (User.email == credentials.username)
    ).first()

    # Check if account is locked
    if user and user.locked_until and user.locked_until > datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account temporarily locked due to failed login attempts. Try again later."
        )

    # Verify password
    if not user or not verify_password(credentials.password, user.hashed_password):
        # Increment login attempts
        if user:
            user.login_attempts += 1
            if user.login_attempts >= 5:
                user.locked_until = datetime.utcnow() + timedelta(minutes=15)
            db.commit()

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled"
        )

    # Reset login attempts on successful login
    user.login_attempts = 0
    user.locked_until = None
    user.last_login = datetime.utcnow()
    db.commit()

    # Create tokens
    access_token = create_access_token(data={"sub": str(user.user_id), "role": user.role.value})
    refresh_token = create_refresh_token(data={"sub": str(user.user_id)})

    # Store refresh token
    refresh_token_obj = RefreshToken(
        user_id=user.user_id,
        token=refresh_token,
        expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    db.add(refresh_token_obj)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


@router.post("/refresh", response_model=Token)
async def refresh_token(
    token_data: TokenRefresh,
    db: Session = Depends(get_db)
) -> Any:
    """
    Refresh an access token using a refresh token.

    - **refresh_token**: Valid refresh token

    Returns new access and refresh tokens.
    """
    # Verify refresh token
    try:
        payload = decode_token(token_data.refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )

    # Check if refresh token exists and is not revoked
    refresh_token_obj = db.query(RefreshToken).filter(
        RefreshToken.token == token_data.refresh_token,
        RefreshToken.revoked == False
    ).first()

    if not refresh_token_obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or revoked refresh token"
        )

    # Get user
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )

    # Revoke old refresh token
    refresh_token_obj.revoked = True
    refresh_token_obj.revoked_at = datetime.utcnow()

    # Create new tokens
    access_token = create_access_token(data={"sub": str(user.user_id), "role": user.role.value})
    new_refresh_token = create_refresh_token(data={"sub": str(user.user_id)})

    # Store new refresh token
    new_refresh_token_obj = RefreshToken(
        user_id=user.user_id,
        token=new_refresh_token,
        expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    db.add(new_refresh_token_obj)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


@router.post("/logout")
async def logout(
    token_data: TokenRefresh,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Logout by revoking the refresh token.

    - **refresh_token**: Refresh token to revoke
    """
    # Revoke refresh token
    refresh_token_obj = db.query(RefreshToken).filter(
        RefreshToken.token == token_data.refresh_token,
        RefreshToken.user_id == current_user.user_id,
        RefreshToken.revoked == False
    ).first()

    if refresh_token_obj:
        refresh_token_obj.revoked = True
        refresh_token_obj.revoked_at = datetime.utcnow()
        db.commit()

    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get current authenticated user information.

    Requires valid JWT token in Authorization header.
    """
    return current_user


@router.post("/api-key", response_model=APIKeyResponse)
async def create_api_key(
    api_key_data: APIKeyCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Generate a new API key for programmatic access.

    Requires authentication. The API key will only be shown once.

    - **name**: Descriptive name for the API key
    """
    # Generate API key
    api_key = generate_api_key()
    hashed_key = hash_api_key(api_key)

    # Update user with hashed API key
    current_user.api_key = hashed_key
    db.commit()

    return {
        "api_key": api_key,
        "user_id": current_user.user_id,
        "created_at": datetime.utcnow(),
        "note": "Store this API key securely. It will not be shown again."
    }


@router.delete("/api-key")
async def revoke_api_key(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Revoke the current user's API key.

    Requires authentication.
    """
    current_user.api_key = None
    db.commit()

    return {"message": "API key revoked successfully"}


@router.post("/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Change the current user's password.

    - **current_password**: Current password
    - **new_password**: New password (min 8 chars, must include uppercase, lowercase, and digit)
    """
    # Verify current password
    if not verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password"
        )

    # Check if new password is different
    if password_data.current_password == password_data.new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be different from current password"
        )

    # Update password
    current_user.hashed_password = hash_password(password_data.new_password)
    db.commit()

    return {"message": "Password changed successfully"}
