"""
stats_service.py

Computes user-facing progress metrics from ReviewLog data.

Primary Responsibilities:
- Calculate counts and summary statistics for display (e.g., due cards, new cards introduced,
  reviews completed today, total reviews, streaks if implemented).
- Provide data in simple, template-friendly structures (dicts/lists/numbers).
- Encapsulate all "how do we compute this metric?" logic in one place.

This service exists to keep statistics logic out of:
- Blueprints (web layer)
- Templates (presentation layer)
- Review service (workflow orchestration)

It SHOULD:
- Read from the database models needed to compute metrics (Card, ReviewLog, etc.).
- Return simple computed values that templates can render directly.
- Keep metric definitions consistent across the app (single source of truth).

It SHOULD NOT:
- Handle HTTP requests, sessions, redirects, or template rendering.
- Perform scheduling updates or review workflow logic (review_service handles that).
- Call external APIs (GPT/TTS) or trigger content generation.
- Define database schema (models handle that).

Architectural Position:

Blueprint (stats page endpoint) → stats_service → models (Card, ReviewLog, User, etc.)

Key Concept:
stats_service answers "what are the numbers?".
It does not change learning state; it only reports it.
"""

from __future__ import annotations

from datetime import datetime, timezone, timedelta
from typing import Optional

from sqlmodel import select, col, func

from app.db import get_session
from app.models.review_log import ReviewLog
from app.models.review_state import ReviewState


def get_session_stats(user_id: int) -> dict:
    """
    Compute review stats for the current session (today, UTC).

    Returns:
        {
            "total_reviewed": int,
            "counts": { "again": int, "hard": int, "good": int, "easy": int },
            "current_streak": int,
            "max_streak": int,
            "cards_due": int,
        }
    """
    session = get_session()
    try:
        # "Today" = since midnight UTC
        now = datetime.now(timezone.utc)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

        # All reviews today, ordered chronologically
        statement = (
            select(ReviewLog)
            .where(ReviewLog.user_id == user_id)
            .where(col(ReviewLog.reviewed_at) >= today_start)
            .order_by(col(ReviewLog.reviewed_at).asc())
        )
        reviews = session.exec(statement).all()

        # Rating counts
        counts = {"again": 0, "hard": 0, "good": 0, "easy": 0}
        rating_map = {1: "again", 2: "hard", 3: "good", 4: "easy"}

        current_streak = 0
        max_streak = 0

        for review in reviews:
            name = rating_map.get(review.rating)
            if name:
                counts[name] += 1

            # Streak: Good or Easy increments, anything else resets
            if review.rating in (3, 4):
                current_streak += 1
                if current_streak > max_streak:
                    max_streak = current_streak
            else:
                current_streak = 0

        # Cards still due
        cards_due_stmt = (
            select(func.count())
            .select_from(ReviewState)
            .where(ReviewState.user_id == user_id)
            .where(col(ReviewState.due_date) <= now)
        )
        cards_due = session.exec(cards_due_stmt).one()

        return {
            "total_reviewed": len(reviews),
            "counts": counts,
            "current_streak": current_streak,
            "max_streak": max_streak,
            "cards_due": cards_due,
        }
    finally:
        session.close()
