"""Fastapp Auth Utilities

Author: Collin Meyer
Created: 2024-01-11 22:21
"""
from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError

from fastapp.auth.users import get_user
from fastapp.auth.password import verify_password
from fastapp.core.settings import get_settings
from fastapp.core.logging import get_logger

settings = get_settings()
logger = get_logger(__name__)


def authenticate_user(
    db, password: str, uid: int = None, name: str = None, email: str = None
):
    """Authenticate a user

    One of uid, name, or email must be specified

    Args:
        db (SessionLocal): The database connection
        password (str): The user's password
        uid (int, optional): The user's id. Defaults to None.
        name (str, optional): The user's name. Defaults to None.
        email (str, optional): The user's email. Defaults to None.
    """
    user = get_user(db, uid, name, email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Create an access token

    Args:
        data (dict): The data to encode
        expires_delta (timedelta, optional): The expiration time. Defaults to None.

    Returns:
        str: The encoded JWT
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.jwt_encode_algorithm
    )

    return encoded_jwt


def create_reset_token(data: dict, expires_delta: timedelta | None = None):
    """Create an access token

    Args:
        data (dict): The data to encode
        expires_delta (timedelta, optional): The expiration time. Defaults to None.

    Returns:
        str: The encoded JWT
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=10)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.jwt_encode_algorithm
    )

    return encoded_jwt


def validate_reset_token(token: str) -> str:
    """Validate a reset token

    Args:
        token (str): The reset token JWT encoded

    Returns:
        str: The user's email or None if the token is invalid
    """
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.jwt_encode_algorithm]
        )
        email: str = payload.get("sub")

    except JWTError as exc:
        logger.debug("Invalid reset token attempted: %s", exc)
        return None

    return email
