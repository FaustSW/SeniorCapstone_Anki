"""
Database configuration and session helpers.

This module is the single source of truth for all database connectivity:
- DB_URL (where the SQLite .db file lives)
- the shared SQLModel engine
- creating Sessions
- initializing tables (create_all)

All runtime code (blueprints, services) and setup scripts (init_db, seed_db)
must import engine/session helpers from here.

Do not call create_engine() anywhere else in the codebase.
Keeping DB configuration centralized prevents inconsistent DB paths and
ensures everyone is reading/writing the same SQLite file.
"""

DB_URL = "sqlite:///./data/app.db"
