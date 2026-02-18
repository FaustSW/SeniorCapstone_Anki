"""
Service Layer Overview

This package contains the core business logic of the application.

Services are responsible for implementing application behavior and workflows.
They are called by blueprints (web layer) and may read/write models (database layer).
They may also call external API clients when needed.

Services SHOULD:
- Implement application rules and decision-making logic.
- Orchestrate workflows (e.g., review flow, generation flow).
- Coordinate between models and external clients.
- Centralize scheduling, regeneration, and statistics logic.
- Return clean, structured data to the calling blueprint.

Services SHOULD NOT:
- Handle HTTP requests or Flask routing logic.
- Render templates or return Flask response objects.
- Contain raw third-party API request code (use clients for that).
- Define database schema (models handle that).
- Implement low-level SM-2 math (use scheduler_adapter).

Architectural Flow:

Blueprints (web layer)
    ↓
Services (business logic)
    ↓
Models (database) + Clients (external APIs)

The service layer is the "brain" of the system.
All application rules should live here to keep the architecture modular and maintainable.
"""
