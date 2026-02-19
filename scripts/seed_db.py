"""
Database Seeding Script

Populates the Vocab table using entries from data/seed_vocab.json.

This script is intentionally thin. Database configuration and session creation
live in app/db.py and must not be duplicated here.

Responsibilities:
- Read the static vocabulary dataset.
- Insert vocab records into the database.
- Preserve intro_index ordering.
- Avoid duplicating entries if re-run (when possible).

Typically run after scripts/init_db.py during development setup.
"""
