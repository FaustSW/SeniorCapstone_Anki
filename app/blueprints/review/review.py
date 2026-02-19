"""
Review Blueprint

Handles the interactive learning experience.

Role:
- Display the next review card.
- Accept and forward user rating submissions.
- Connect user actions to the review workflow in the service layer.

This blueprint represents the core study loop of the application.
"""
from flask import Blueprint, render_template, request, jsonify
import random

review_bp = Blueprint('review', __name__, template_folder='templates')
# Review page, where you view cards and mark them as known/unknown

# For HTML generation testing, to be removed later
random_words = [
    "Ephemeral", "Komorebi", "Fernweh", "Taciturno", "Bibliothèque",
    "Sempiternal", "Saudade", "Schadenfreude", "Murciélago", "Tsundoku",
    "Labyrinth", "Petrichor", "Ziggurat", "Querencia", "Hiraeth",
    "Oubliette", "Waldeinsamkeit", "Mellifluous", "Ikigai", "Gula",
    "Vellichor", "Inmarcesible", "Chiaroscuro", "Kintsugi", "L’appel du vide",
    "Serendipity", "Doppelgänger", "Sobremesa", "Ukiyo", "Ethereal",
    "Flâneur", "Wanderlust", "Ataraxia", "Pamplemousse", "Nadir",
    "Cachivache", "Kenshō", "Bruma", "Sonder", "Torschlusspanik",
    "Susurrus", "Mono no aware", "Dépaysement", "Heimat", "Ojala",
    "Ineffable", "Yūgen", "Cafuné", "Gezellig", "Glück"
]

# Review page, where you view cards and mark them as known/unknown
@review_bp.route('/', methods=['GET'])
def generate_cards():
    selected_words = random.choice(random_words) # Simulate card generation with random words
    selected_words2 = random.choice(random_words) # Simulate card generation with random words
    # This will be the main interface for reviewing cards
    return render_template('card.html', main_text_placeholder=selected_words, back_text_placeholder=selected_words2) 

@review_bp.route('/handle_card_response', methods=['POST'])
def handle_card_response():
    data = request.get_json()
    response = data.get('action')
    # Here you would process the user's response and update your spaced repetition algorithm
    print(f"User marked the card as: {response}")
    return jsonify({"status": "success"})