"""
This service acts as a translation layer between our Card model
and the external SM-2 scheduling implementation.

Primary Responsibilities:
- Convert Card scheduling fields into the format expected by the SM-2 library.
- Pass the user's review rating to the scheduler.
- Receive updated scheduling values from the scheduler.
- Return updated scheduling fields in a format compatible with our Card model.

This service treats SM-2 as a black box.
It does not implement scheduling math itself.

It SHOULD:
- Be the only place in the codebase that interacts directly with the SM-2 library.
- Translate between our internal field names and the scheduler's data structure.
- Return updated values (interval, ease_factor, repetitions, lapses, due_date, etc.)
  without directly persisting them.

It SHOULD NOT:
- Select which card to review (review_service handles that).
- Handle HTTP requests or Flask routing.
- Call external APIs (GPT/TTS).
- Contain business workflow logic.
- Define database schema (models handle that).

Architectural Position:

review_service → scheduler_adapter → SM-2 library (black box)

Key Concept:
scheduler_adapter isolates the scheduling algorithm from the rest of the system.
If we ever swap out SM-2, only this file should need modification.
"""