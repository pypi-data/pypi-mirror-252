"""Fastapp Database Schema
Schematics for objects in the database

Author: Collin Meyer
Created: 2024-01-11 22:21
"""
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()


# pylint: disable=too-few-public-methods
class User(Base):
    """User model"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    first = Column(String, nullable=True)
    last = Column(String, nullable=True)
    email = Column(String, index=True, unique=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    logins = Column(Integer, default=0)
