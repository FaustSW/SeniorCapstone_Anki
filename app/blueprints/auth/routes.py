"""
Authentication Blueprint

Handles all user authentication endpoints.

Role:
- Render login and registration pages.
- Process authentication form submissions.
- Manage session state (login/logout).

This blueprint is responsible for user identity and access to the system.
"""
from flask import Blueprint, render_template, request, redirect, url_for, session

auth_bp = Blueprint('auth', __name__, template_folder='templates')

# Home page, includes profiles, settings, and navigation to other sections 
@auth_bp.route('/')
def index():
    return render_template('login.html') 

# TODO: Add url_for redirect to review page after successful login
@auth_bp.route('/go_to_review')
def go_to_review():
    return redirect(url_for('review.generate_cards'))