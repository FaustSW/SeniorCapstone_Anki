"""
Blueprints Package

This package contains the Flask Blueprint modules that define the web layer
of the application (auth, review, stats).

What is a Blueprint?
In Flask, a Blueprint is a modular grouping of related routes (endpoints).
Each blueprint defines a set of URL paths and HTTP methods, and is later
registered with the main Flask application in the app factory.

Blueprints are responsible for:
- Reading request data (form fields, query params).
- Managing sessions (via Flask).
- Calling services to perform business logic.
- Returning rendered templates or redirects.

This package contains no business logic, only web-facing route definitions.
"""
