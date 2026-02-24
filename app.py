from flask import Flask, render_template, request, jsonify
from app.blueprints.login.auth import auth_bp   # Import the authentication blueprint
from app.blueprints.review.review import review_bp # Import the review blueprint
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

if __name__ == '__main__':
    app.run(debug=True)