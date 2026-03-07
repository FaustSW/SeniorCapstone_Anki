"""
Review Blueprint

Handles the interactive learning experience.

Routes:
    GET  /review/     — load first due card and render the review page
    POST /review/rate — process a rating, return next card as JSON
"""
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for

from app.services.review_service import get_next_card, process_review
from app.services.stats_service import get_session_stats

review_bp = Blueprint('review', __name__, template_folder='templates')


@review_bp.route('/', methods=['GET'])
def generate_cards():
    """Load the review page with the first due card."""
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.index'))

    card = get_next_card(user_id)
    stats = get_session_stats(user_id)

    return render_template(
        'review.html',
        card=card,
        stats=stats,
    )


@review_bp.route('/rate', methods=['POST'])
def rate_card():
    """Process a rating and return the next card as JSON."""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json(force=True)
    review_state_id = data.get('review_state_id')
    rating = data.get('rating')

    if review_state_id is None or rating is None:
        return jsonify({"error": "review_state_id and rating are required"}), 400

    try:
        rating = int(rating)
        result = process_review(user_id, int(review_state_id), rating)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    # Get the next card and updated stats
    next_card = get_next_card(user_id)
    stats = get_session_stats(user_id)

    return jsonify({
        "result": result,
        "next_card": next_card,
        "stats": stats,
    })