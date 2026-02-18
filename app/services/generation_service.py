"""
This service manages the lifecycle of AI-generated content for review cards
(example sentences, translations, and audio).

Primary Responsibilities:
- Determine whether generated content is needed for a card.
- Apply regeneration rules (based on card scheduling state).
- Construct prompts for LLM generation.
- Call external API clients (gpt_client, elevenlabs_client).
- Validate and normalize responses.
- Persist generated content to the database (caching results).
- Return a display-ready content bundle to the calling service.

Regeneration Policy:
Regeneration rules (e.g., based on success_streak and interval thresholds)
are currently defined and enforced within this service. If regeneration
logic becomes more complex or reused elsewhere, it may be extracted into
a dedicated service.

This service owns both the decision and execution of content generation.

It SHOULD:
- Decide when to call GPT.
- Decide when to call TTS.
- Centralize regeneration and caching policy.
- Coordinate persistence of generated fields.
- Return structured data suitable for templates.

It SHOULD NOT:
- Handle HTTP routing or Flask request/response logic (blueprints handle that).
- Implement scheduling math (scheduler_adapter handles that).
- Select which card to review (review_service handles that).
- Contain raw API transport logic (clients handle external requests).
- Define database schema (models handle that).

Architectural Position:

Blueprint → review_service → generation_service → clients (GPT/TTS) → models (cache persistence)

Key Concept:
generation_service is the content lifecycle manager.
It decides when content must exist and ensures it does.
"""
