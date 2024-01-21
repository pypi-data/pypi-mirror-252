"""Fastapp Auth Routes
All routes relating to authentication for fastapp

Author: Collin Meyer
Created: 2024-01-13 12:56
"""
import csv
import json
from io import StringIO
from typing import Annotated
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import update, func

from fastapp.db.db import get_db
from fastapp.db.schema import User as DBUser
from fastapp.core.models.auth import Token, Grant, PasswordReset
from fastapp.core.models.user import User, CreateUser, DeleteUser, SignupUser, UserList
from fastapp.core.settings import get_settings
from fastapp.core.logging import get_logger
from fastapp.core.mail import send_reset_email
from fastapp.auth.auth import (
    authenticate_user,
    create_access_token,
    create_reset_token,
    validate_reset_token,
)
from fastapp.auth.password import get_password_hash
from fastapp.auth.users import (
    get_current_active_user,
    get_current_admin_user,
    get_all_users,
    create_user,
    delete_user,
)

router = APIRouter(prefix="/auth", tags=["Users and Authentication"])
settings = get_settings()

logger = get_logger(__name__)


@router.post("/token")
async def login_for_access_token(
    db: Annotated[Session, Depends(get_db)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """Get an OAuth2 token for a user

    Args:
        db (SessionLocal): The database connection
        form_data (OAuth2PasswordRequestForm): The form data from the request

    Raises:
        HTTPException: If the user is not authenticated

    Returns:
        Token: The OAuth2 token
    """
    if "@" in form_data.username:
        user = authenticate_user(
            db, email=form_data.username, password=form_data.password
        )
    else:
        user = authenticate_user(
            db, name=form_data.username, password=form_data.password
        )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire)
    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )

    grants = [Grant.USER]
    if user.is_admin:
        grants.append(Grant.ADMIN)

    db.execute(update(DBUser), [{"id": user.id, "logins": user.logins + 1}])
    db.commit()
    db.refresh(user)

    return Token(access_token=access_token, token_type="bearer", grants=grants)

if settings.signup_enabled:
    @router.post("/signup")
    async def signup_user(
        db: Annotated[Session, Depends(get_db)],
        signup_config: SignupUser,
    ) -> User:
        """Signup a new user

        Args:
            db (SessionLocal): The database connection
            signup_config (SignupUser): The signup config

        Returns:
            User: The new user
        """
        user = create_user(db, CreateUser(**signup_config.model_dump()))

        if user is None:
            raise HTTPException(409, "Username or email already exists")

        return user


@router.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> User:
    """Get info about currently logged in user"""
    return current_user


# pylint: disable=unused-argument
# pylint: disable=too-many-arguments
@router.get("/users/")
async def get_users(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_admin_user)],
    skip: int = 0,
    limit: int = 100,
    search: str = None,
    is_admin: bool = None,
) -> UserList:
    """Get all users

    Admin only interface for managing user base
    """

    if search is None:
        count = db.query(DBUser).filter(DBUser.is_admin == is_admin).count()
        return UserList(
            users = await get_all_users(db, skip, limit, is_admin),
            count = count
        )

    results = db.query(DBUser).filter(
        DBUser.name.like(f'%{search}%') |
        DBUser.email.like(f'%{search}%') |
        DBUser.first.like(f'%{search}%') |
        DBUser.last.like(f'%{search}%')
    )

    count = results.count()
    items = results.offset(skip).limit(limit).all()
    return UserList(
        users = items,
        count = count
    )


@router.get("/logins/")
async def get_logins(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_admin_user)],
) -> int:
    """Get Number of User Logins

    Admin only interface
    """

    return db.query(func.sum(DBUser.logins)).scalar()


# pylint: disable=unused-argument
@router.post("/user/")
def create_user_endpoint(
    db: Annotated[Session, Depends(get_db)],
    create_config: CreateUser,
    current_user: Annotated[User, Depends(get_current_admin_user)],
) -> User:
    """Create a new user

    Admin only interface for managing user base
    """

    user = create_user(db, create_config)

    if user is None:
        raise HTTPException(409, "Username or email already exists")

    return user


@router.post("/users/")
async def create_users_endpoint(
    db: Annotated[Session, Depends(get_db)],
    file: UploadFile,
    filetype: Annotated[str, Form()],
    current_user: Annotated[User, Depends(get_current_admin_user)],
) -> list[User]:
    """Create a new user

    Admin only interface for managing user base
    """

    if filetype == "JSON":
        try:
            data = json.loads((await file.read()).decode("utf-8"))
        except Exception as e:
            raise HTTPException(422, "Invalid JSON file") from e
    elif filetype == "CSV":
        try:
            f = StringIO((await file.read()).decode("utf-8"))
            data = csv.DictReader(f)
        except Exception as e:
            logger.exception("Error reading CSV file: %s", e)
            raise HTTPException(422, "Invalid CSV file") from e
    else:
        raise HTTPException(422, "Invalid filetype")

    # user = create_user(db, create_config)
    new_users = []
    for row in data:
        new_user = CreateUser(**row)

        user = create_user(db, new_user)
        if user is None:
            raise HTTPException(409, "username or email already exists")
        new_users.append(user)

    return new_users


@router.delete("/user/")
def delete_user_endpoint(
    db: Annotated[Session, Depends(get_db)],
    delete_config: DeleteUser,
    current_user: Annotated[User, Depends(get_current_admin_user)],
) -> User:
    """Delete a user

    Admin only interface for managing user base
    """

    user = delete_user(db, delete_config)

    return user


@router.get("/user/reset-password")
async def request_reset_user_password(
    db: Annotated[Session, Depends(get_db)],
    email: str,
):
    """Reset a user's password"""
    user = db.query(DBUser).filter(DBUser.email == email).first()

    if user is None:
        raise HTTPException(404, "User not found")

    reset_token = create_reset_token({"sub": user.email}, timedelta(minutes=10))

    await send_reset_email(user.email, user.name, reset_token)
    return {}


@router.post("/user/do-reset-password")
async def reset_user_password(
    db: Annotated[Session, Depends(get_db)],
    password_config: PasswordReset,
):
    """Reset a user's password"""

    email = validate_reset_token(password_config.token)

    if email is None:
        raise HTTPException(404, "Reset invalid or expired")

    user = db.query(DBUser).filter(DBUser.email == email).first()

    if user is None:
        raise HTTPException(404, "User to reset not found")

    db.execute(
        update(DBUser),
        [
            {
                "id": user.id,
                "password": get_password_hash(password_config.password),
            }
        ],
    )
    db.commit()
    db.refresh(user)

    return {}
