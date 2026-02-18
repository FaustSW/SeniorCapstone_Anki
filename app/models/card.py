"""
Database Model: Card

Represents a user-specific learning state for a single Vocab item.

Core Fields:
- id: primary key
- user_id: foreign key to User
- vocab_id: foreign key to Vocab

Scheduling Fields (SM-2 state):
- ease_factor
- interval
- repetitions
- lapses
- due_date
- success_streak

Generated Content Cache:
- sentence_cached
- translation_cached
- audio_path
- generated_at (timestamp for last generation)

This model evolves as the user reviews cards.
It is the central state object of the learning system.
"""
