from flask import Flask, render_template, request, jsonify
from app.blueprints.login.auth import auth_bp   # Import the authentication blueprint
from app.blueprints.review.review import review_bp # Import the review blueprint
from themes import themes, DEFAULT_THEME # Import themes and default theme
from app.blueprints.stats.stats import stats_bp # Import the stats blueprint

# from core_logic import AnkiGenerator # Assuming this is your main class/function

app = Flask(__name__,
            template_folder="app/templates",
            static_folder="app/static")

app.register_blueprint(auth_bp)  # Register the authentication blueprint
app.register_blueprint(review_bp, url_prefix='/review') # Register the review blueprint
app.register_blueprint(stats_bp, url_prefix='/stats') # Register the stats blueprint


# Simple API endpoints
@app.route('/api/health')
def api_health():
    return jsonify({"status": "ok"})


@app.route('/api/review/next')
def api_review_next():
    return jsonify({
        "card_id": 1,
        "spanish": "hola",
        "english": "hello"
    })


@app.route('/api/review/<int:card_id>', methods=['POST'])
def api_review_grade(card_id):
    data = request.get_json()
    rating = data.get("rating", 2)

    return jsonify({
        "card_id": card_id,
        "rating": rating,
        "message": "Review saved (demo stub)",
        "next_due_days": 3
    })


# ============================================================================================================== 
# THEME ROUTES - For theme switching functionality
# ============================================================================================================== 

# Route to get all available themes
@app.route('/api/themes', methods=['GET'])
def get_themes():
    theme_list = []
    for theme_key, theme_data in themes.items():
        theme_list.append({
            'id': theme_key,
            'name': theme_data['name']
        })
    return jsonify(theme_list)

# Route to get specific theme colors
@app.route('/api/theme/<theme_id>', methods=['GET'])
def get_theme(theme_id):
    if theme_id in themes:
        return jsonify(themes[theme_id])
    return jsonify({'error': 'Theme not found'}), 404

# Route to save user's theme preference
@app.route('/api/save-theme', methods=['POST'])
def save_theme():
    data = request.json
    theme_id = data.get('theme_id')
    
    if theme_id in themes:
        return jsonify({'success': True, 'theme': theme_id})
    return jsonify({'success': False, 'error': 'Invalid theme'}), 400


if __name__ == '__main__':
    app.run(debug=True)