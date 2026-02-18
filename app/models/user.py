"""
Database Model: User

Represents a registered account in the system.

Core Fields:
- id: primary key
- username/identifier: unique display/login name
- password_hash: securely hashed password
- created_at: account creation timestamp

This model stores identity and authentication data only.
Each user will have many associated Card records.
"""
