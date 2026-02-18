"""
External API Clients Package

This package contains thin wrappers around third-party services
(e.g., LLM providers, TTS providers).

Clients are responsible only for:
- Sending requests to external APIs.
- Handling authentication/configuration.
- Returning raw or minimally processed responses.

Clients SHOULD NOT:
- Contain business logic.
- Decide when an API should be called.
- Implement caching or regeneration rules.
- Perform database reads/writes.
- Know anything about Flask, sessions, or templates.

All decision-making and orchestration belongs in the service layer.
Clients are transport-only adapters to external systems.
"""
