"""
This service owns the end-to-end "review loop" workflow for a user.

Primary Responsibilities:
- Select the next card to review for a user (typically the earliest due card).
- Prepare a display-ready card payload for the UI (may request generated content via generation_service).
- Process a submitted review rating (Again/Hard/Good/Easy or equivalent).
- Update the card's scheduling state by delegating to scheduler_adapter (SM-2 black box).
- Record review history events (e.g., ReviewLog) for statistics and auditing.
- Coordinate optional content generation decisions (via regen_service / generation_service).

This is the orchestration layer for reviewing:
it coordinates models + scheduler + generation, but does not implement their internals.

It SHOULD:
- Contain the rules for "what happens during a review session".
- Call scheduler_adapter to update scheduling fields after a rating.
- Call generation_service to ensure sentence/translation/audio exist when needed.
- Read/write the Card model (and ReviewLog if used).
- Return simple Python data structures for templates (not Flask responses).

It SHOULD NOT:
- Handle HTTP routing, sessions, or request parsing (blueprints handle that).
- Render templates or return Flask Response objects.
- Make direct external API calls (use generation_service → clients).
- Implement SM-2 scheduling math (scheduler_adapter handles that).
- Define database schema (models handle that).

Architectural Position:

Blueprint (review endpoints) → review_service  →  scheduler_adapter (SM-2 update)
    →  generation_service → clients (GPT/TTS) →  models (Card, Vocab, ReviewLog)

Key Concept:
review_service decides the workflow: "pick card → show content → accept rating → update state".
Other services/clients provide specialized functionality when asked.
"""
