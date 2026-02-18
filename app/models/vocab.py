"""
Database Model: Vocab

Represents a vocabulary item from the seeded dataset.
This is global content shared across all users.

Core Fields:
- id: primary key
- term: spanish word or expression (e.g., "hola")
- english_gloss: short meaning/definition/translation
- intro_index: integer controlling introduction order

This table does not store user-specific learning state.
User progress is tracked in the Card model.
"""
