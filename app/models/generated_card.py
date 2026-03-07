"""
Database Model: GeneratedCard

A single generated display artifact for a ReviewState.

Stores the sentence, translation, and audio path that the user
sees during review. Created by generation_service (future).

A ReviewState can have many GeneratedCards over its lifetime
(one per regeneration). The active one is tracked via
ReviewState.current_generated_card_id.

For now: table exists, fields defined, no generation logic wired.
Generation service will populate this when AI integration is ready.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from sqlmodel import SQLModel, Field


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class GeneratedCard(SQLModel, table=True):

    __tablename__ = "generated_card"

    id:              Optional[int] = Field(default=None, primary_key=True)
    review_state_id: int           = Field(foreign_key="review_state.id", index=True)

    # Snapshots of what the user saw (denormalized from Vocab at generation time)
    term_snapshot:         str
    english_gloss_snapshot: str

    # Generated content (empty until generation_service is wired)
    sentence:      Optional[str] = Field(default=None)
    translation:   Optional[str] = Field(default=None)
    tts_audio_path: Optional[str] = Field(default=None)

    generation_number: int = Field(default=1)
    created_at: datetime   = Field(default_factory=utcnow)