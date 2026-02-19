"""
Database Initialization Script

Initializes the SQLite database and creates all tables defined in app.models.

This script is intentionally thin. Database configuration and engine creation
live in app/db.py and must not be duplicated here.

Responsibilities:
- Ensure the database directory exists if the DB file is under a folder (e.g. data/).
- Call app.db.init_db() to create all required tables.
- Be safe to run multiple times without duplicating tables.

Intended for initial setup and for resetting to a fresh database during development.
"""
