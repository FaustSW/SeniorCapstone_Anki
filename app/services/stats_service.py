"""
This service computes user-facing progress metrics for the application.

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
