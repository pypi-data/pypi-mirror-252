"""Fastapp User Models
Pydantic models for user returning, creation, etc.

Author: Collin Meyer
Created: 2024-01-13 15:09
"""

from pydantic import BaseModel, ConfigDict


# pylint: disable=too-few-public-methods
# pylint: disable=missing-class-docstring
class User(BaseModel):
    name: str
    email: str
    first: str | None
    last: str | None
    is_active: bool
    is_admin: bool

    model_config = ConfigDict(from_attributes=True)


class CreateUser(BaseModel):
    name: str
    email: str
    password: str
    first: str = None
    last: str = None
    is_admin: bool = False
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)


class SignupUser(BaseModel):
    name: str
    first: str
    last: str
    email: str
    password: str

    model_config = ConfigDict(from_attributes=True)


class DeleteUser(BaseModel):
    uid: int | None = None
    name: str | None = None
    email: str | None = None

    model_config = ConfigDict(from_attributes=True)

class UserList(BaseModel):
    users: list[User]
    count: int

    model_config = ConfigDict(from_attributes=True)
