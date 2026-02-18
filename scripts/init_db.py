"""
Database Initialization Script

Creates the SQLite database file (data/app.db) and initializes all tables
defined in the models package.

Responsibilities:
- Ensure the data/ directory exists.
- Create the database if it does not already exist.
- Create all required tables (User, Vocab, Card, ReviewLog).
- Be safe to run multiple times without duplicating tables.

This script is intended to be run once during initial project setup,
or whenever a fresh database is needed.
"""
