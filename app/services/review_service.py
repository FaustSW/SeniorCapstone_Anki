"""
review_service.py

Owns the end-to-end "review loop" workflow for a user.

Primary responsibilities:
    - Select the next card to review (earliest due date).
    - Prepare a display-ready card payload for the template.
    - Process a submitted rating (Again/Hard/Good/Easy).
    - Update the card's scheduling state via scheduler_adapter.
    - Update app-owned counters (repetitions, lapses, success_streak).
    - Log review events to ReviewLog for stats.

This is the orchestration layer for reviewing. It coordinates
models + scheduler + (eventually) generation, but does not
implement their internals.

Architectural position:
    Blueprint (review.py) -> review_service -> scheduler_adapter (SM-2)
                                            -> models (ReviewState, Vocab, ReviewLog)
                                            -> generation_service (future, for AI sentences)
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from sqlmodel import select, col

from app.db import get_session
from app.models.review_state import ReviewState
from app.models.vocab import Vocab
from app.models.review_log import ReviewLog
from app.services.scheduler_adapter import SchedulerAdapter


# Single shared scheduler instance for the app.
# Created once here so every call to review_service uses the same config.
_scheduler = SchedulerAdapter()


# ------------------------------------------------------------------
# Core review loop
# ------------------------------------------------------------------

def get_next_card(user_id: int) -> Optional[dict]:
    """
    Return the next card for this user to review, or None if nothing is due.

    Returns a dict with everything the template needs to render a card:
        {
            "review_state_id": int,
            "vocab_id": int,
            "term": str,
            "english_gloss": str,
            "sentence": str or None,       # populated by generation_service (future)
            "translation": str or None,    # populated by generation_service (future)
            "audio_path": str or None,     # populated by generation_service (future)
        }
    """
    session = get_session()
    try:
        review_state = _get_due_review_state(session, user_id)

        if review_state is None:
            return None

        vocab = session.get(Vocab, review_state.vocab_id)

        return {
            "review_state_id": review_state.id,
            "vocab_id": review_state.vocab_id,
            "term": vocab.term,
            "english_gloss": vocab.english_gloss,
            "sentence": None,
            "translation": None,
            "audio_path": None,
        }
    finally:
        session.close()


def process_review(user_id: int, review_state_id: int, rating: int) -> dict:
    """
    Process a user's rating for a review state and return the updated state.

    Loads the ReviewState, verifies ownership, runs the rating through
    scheduler_adapter, updates app-owned counters, logs to ReviewLog,
    and commits everything in one transaction.

    rating: int in {1, 2, 3, 4} -> Again, Hard, Good, Easy.

    Returns a dict with review_state_id, rating, new_interval,
    new_due_date (ISO string), and success_streak.
    """
    if rating not in (1, 2, 3, 4):
        raise ValueError(f"Invalid rating: {rating!r} (expected 1-4)")

    session = get_session()
    try:
        review_state = session.get(ReviewState, review_state_id)
        if review_state is None:
            raise ValueError(f"ReviewState {review_state_id} not found")
        if review_state.user_id != user_id:
            raise ValueError(f"ReviewState {review_state_id} does not belong to user {user_id}")

        # Run through the SM-2 scheduler (mutates review_state in place)
        _scheduler.apply_review(review_state, rating)

        # Update app-owned counters
        _update_app_counters(review_state, rating)

        # Log the review event
        log_entry = ReviewLog(
            user_id=user_id,
            review_state_id=review_state.id,
            vocab_id=review_state.vocab_id,
            rating=rating,
        )
        session.add(log_entry)

        # Commit review_state updates and the log entry together
        session.add(review_state)
        session.commit()

        return {
            "review_state_id": review_state.id,
            "rating": rating,
            "new_interval": review_state.interval,
            "new_due_date": review_state.due_date.isoformat(),
            "success_streak": review_state.success_streak,
        }
    finally:
        session.close()


# ------------------------------------------------------------------
# ReviewState selection
# ------------------------------------------------------------------

def _get_due_review_state(session, user_id: int) -> Optional[ReviewState]:
    """
    Return the user's ReviewState with the earliest due_date at or before now.
    Returns None if nothing is due.
    """
    now = datetime.now(timezone.utc)
    statement = (
        select(ReviewState)
        .where(ReviewState.user_id == user_id)
        .where(col(ReviewState.due_date) <= now)
        .order_by(col(ReviewState.due_date).asc())
        .limit(1)
    )
    return session.exec(statement).first()


# ------------------------------------------------------------------
# App-owned counter updates
# ------------------------------------------------------------------

def _update_app_counters(review_state: ReviewState, rating: int) -> None:
    """
    Update the counters that live on ReviewState but aren't touched by
    the scheduler_adapter (repetitions, lapses, success_streak).
    """
    review_state.repetitions += 1

    # A lapse is when a Review-state card gets an Again rating.
    # After the scheduler runs, a lapsed card moves to Relearning (state 3),
    # so we check the post-review scheduler_state.
    if rating == 1 and review_state.scheduler_state == 3:
        review_state.lapses += 1

    # Success streak tracks consecutive Good/Easy ratings for regeneration logic
    if rating in (3, 4):
        review_state.success_streak += 1
    else:
        review_state.success_streak = 0
