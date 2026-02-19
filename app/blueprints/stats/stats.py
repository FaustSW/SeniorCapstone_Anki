"""
Statistics Blueprint

Handles progress and performance endpoints.

Role:
- Render user progress metrics and summary views.
- Request computed statistics from the service layer.
- Present learning data to the user.

This blueprint represents the reporting side of the system.
"""

from flask import Blueprint, render_template, request, jsonify

stats_bp = Blueprint('stats', __name__, template_folder='templates')

# Stats page, where you can see your progress and performance over time
@stats_bp.route('/stats', methods=['GET'])
def stats():
    return render_template('stats.html')
