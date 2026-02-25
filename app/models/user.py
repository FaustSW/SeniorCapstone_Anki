"""
Database Model: User

A registered account in the system.

Fields:
    id            — primary key
    username      — unique login/display name
    password_hash — hashed password (hashing logic lives in auth service, not here)
    created_at    — account creation timestamp (UTC)

This model only stores identity and auth data.
Learning state is tracked per-user through Card records.
Table name is "user" to match Card's foreign_key="user.id".
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from sqlmodel import SQLModel, Field


def utcnow() -> datetime:
    """Return the current time in UTC with timezone info attached."""
    return datetime.now(timezone.utc)


class User(SQLModel, table=True):
    """
    A registered user account.

    Stores identity and auth credentials. Learning state
    is tracked per-user through Card records, not here.
    """

    __tablename__ = "user"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    password_hash: str
    created_at: datetime = Field(default_factory=utcnow)
