"""
init_db.py

Creates all database tables. Safe to run multiple times as
existing tables won't be duplicated.

Usage:
    python -m scripts.init_db
"""

import os
import sys

# Add project root to path so "from app..." imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db import init_db

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    init_db()
    print("Database tables created.")
