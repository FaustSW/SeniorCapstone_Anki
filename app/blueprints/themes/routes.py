import json
import os
from flask import Blueprint, request, jsonify

themes_bp = Blueprint('themes', __name__)

# Load theme data once at import time
_themes_path = os.path.join(os.path.dirname(__file__), 'themes.json')
with open(_themes_path, 'r') as f:
    themes = json.load(f)

DEFAULT_THEME = 'light'


@themes_bp.route('/api/themes', methods=['GET'])
def get_themes():
    theme_list = [
        {'id': key, 'name': data['name']}
        for key, data in themes.items()
    ]
    return jsonify(theme_list)


@themes_bp.route('/api/theme/<theme_id>', methods=['GET'])
def get_theme(theme_id):
    if theme_id in themes:
        return jsonify(themes[theme_id])
    return jsonify({'error': 'Theme not found'}), 404


@themes_bp.route('/api/save-theme', methods=['POST'])
def save_theme():
    data = request.json
    theme_id = data.get('theme_id')
    if theme_id in themes:
        return jsonify({'success': True, 'theme': theme_id})
    return jsonify({'success': False, 'error': 'Invalid theme'}), 400