"""
Database Model: ReviewLog

Represents a single review event for auditing and statistics.

Core Fields:
- id: primary key
- user_id: foreign key to User
- card_id: foreign key to Card
- rating: user rating value (e.g., 0-3 or Again/Hard/Good/Easy)
- reviewed_at: timestamp of the review

This table provides historical data for computing metrics and analytics.
It does not affect scheduling directly.
"""
