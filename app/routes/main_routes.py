from flask import Blueprint, jsonify

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask API!"})

@main_bp.route('/test')
def test():
    return jsonify({"message": "API is working!"})