"""
Database Model: Card

Represents a user-specific learning state for a single Vocab item.

Core Fields:
- id: primary key
- user_id: foreign key to User
- vocab_id: foreign key to Vocab

Scheduling Fields (SM-2 state):
- ease_factor
- interval
- repetitions
- lapses
- due_date
- success_streak

Generated Content Cache:
- sentence_cached
- translation_cached
- audio_path
- generated_at (timestamp for last generation)

This model evolves as the user reviews cards.
It is the central state object of the learning system.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from sqlmodel import SQLModel, Field
from sqlalchemy import UniqueConstraint, Index  # used via __table_args__


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Card(SQLModel, table=True):
    """
    Represents a user-specific learning state for a single Vocab item.

    One (user, vocab) pair -> one Card.
    Central state object of the learning system.
    """

    __tablename__ = "cards"

    __table_args__ = (
        UniqueConstraint("user_id", "vocab_id", name="uq_cards_user_vocab"),
        Index("ix_cards_user_due_date", "user_id", "due_date"),
    )

    # ---------------------------
    # Core Fields
    # ---------------------------
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="user.id", index=True)
    vocab_id: int = Field(foreign_key="vocab.id", index=True)

    # ---------------------------
    # Scheduling Fields (SM-2 state)
    # ---------------------------
    # These are persisted scheduling fields owned by our system.
    # scheduler_adapter translates to/from the SM-2 library.
    ease_factor: float = Field(default=2.5)
    interval: int = Field(default=0)          # days
    repetitions: int = Field(default=0)
    lapses: int = Field(default=0)
    due_date: datetime = Field(default_factory=utcnow, index=True)

    # App-owned scheduling meta
    success_streak: int = Field(default=0)

    # Optional but commonly needed for SM-2 implementations that have learning steps / phases.
    # If your chosen SM-2 lib truly doesn't need them, you can delete these later.
    scheduler_state: Optional[int] = Field(default=1)  # 1=Learning, 2=Review, 3=Relearning
    learning_step: Optional[int] = Field(default=None)

    # ---------------------------
    # Generated Content Cache
    # ---------------------------
    sentence_cached: Optional[str] = Field(default=None)
    translation_cached: Optional[str] = Field(default=None)
    audio_path: Optional[str] = Field(default=None)

    generated_at: Optional[datetime] = Field(default=None)

    # ---------------------------
    # Timestamps
    # ---------------------------
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)
