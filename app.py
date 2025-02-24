from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from supabase import create_client
import os
from flask import Flask

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask API!"})

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    isTeacher = data.get('isTeacher')

    # Use auth to handle password management
    try:
        response = supabase.auth.sign_up({
            "email": username,
            "password": password
        })
    except Exception as e:
        return jsonify({"error": "failed to sign up user"}), 500
    
    try:
        data, count = supabase.table('users').insert(
            [{"user_id": response.user.id, "username": username, "is_teacher": isTeacher}],
            returning="representation"
        ).execute()
        return jsonify({"user_id": response.user.id}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "failed to insert new user into table"}), 500

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    try:
        user = supabase.auth.sign_in_with_password({
            "email": username,
            "password": password
        })
    except Exception as e:
        return jsonify({"error": "failed to fetch from database"}), 500
    return jsonify({"user_id": user.user.id}), 200

@app.route('/api/test')
def test():
    return jsonify({"message": "API is working!"})

@app.route('/api/questions', methods=['GET', 'POST'])
def handle_questions():
    return jsonify({})
# def handle_questions():
#     if request.method == 'POST':
#         # Get the questions from the request body
#         new_questions = request.get_json()
#         if not isinstance(new_questions, list):
#             return jsonify({"error": "Expected a list of questions"}), 400
        
#         # Add the questions to our storage
#         questions.extend(new_questions)
#         print(questions)
#         return jsonify({"message": "Questions added successfully", "count": len(new_questions)}), 201
    
#     # Handle GET request
#     return jsonify({"questions": questions})


if __name__ == '__main__':
    app.run(debug=True) 