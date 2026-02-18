"""
Models Package

This package defines the database schema for the application.

Each model file represents one core entity stored in the database
(e.g., User, Vocab, Card, ReviewLog). Models describe the shape of the data:
fields/columns, relationships, and constraints.

How to think about these entities:
- Vocab: the shared, seeded vocabulary dataset (global content).
- Card: a user-specific learning state for a vocab item (scheduling + cached content).
- User: account identity and authentication fields.
- ReviewLog: optional event history for reviews (useful for stats and auditing).

Models are used by the service layer to store and retrieve application state.
They do not implement application workflows themselves.
"""
