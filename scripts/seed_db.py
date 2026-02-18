"""
Database Seeding Script

Populates the Vocab table using entries from data/seed_vocab.json.

Responsibilities:
- Read the static vocabulary dataset.
- Insert vocab records into the database.
- Preserve intro_index ordering.
- Avoid duplicating entries if re-run (when possible).

This script is run after init_db.py to load the initial vocabulary set.
"""
