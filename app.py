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

@app.route('/api/make_session', methods=['GET', 'POST'])
def make_session():
    data = request.get_json()
    teacher_id = data.get('user_id')
    try:
        response = (supabase.table('sessions').insert(
            [{"teacher_id": teacher_id}],
            returning="representation"
        ).execute())
        return jsonify({"session_id": response.data[0].get('session_id')}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "failed to fetch from database"}), 500

@app.route('/api/test')
def test():
    return jsonify({"message": "API is working!"})

@app.route('/api/save_questions', methods=['POST'])
def save_questions():
    try:
        questions = request.get_json()
        response = (
            supabase.table('questions').insert(
                questions, returning="representation"
            ).execute()
        )
        return jsonify({"questions": response.data, "count": response.count}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "upload failed"}), 500
    
@app.route('/api/get_questions', methods=['POST'])
def get_questions():
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        response = (
            supabase.table('questions').select('*').eq('session_id', session_id).execute()
        )
        return jsonify({"questions": response.data, "count": response.count}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "upload failed"}), 500

@app.route('/api/set_question', methods=['POST'])
def set_question():
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        question_id = data.get('question_id')
        session = (
            supabase.table('sessions').update({'current_question': question_id}).eq('session_id', session_id).execute()
        )
        return jsonify({"session": session.data[0]}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "upload failed"}), 500

@app.route('/api/current_question', methods=['POST'])
def current_question():
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        session = (
            supabase.table('sessions').select('*').eq('session_id', session_id).execute()
        )
        question_id = session.data[0]['current_question']
        question = (
            supabase.table('questions').select('*').eq('question_id', question_id).execute()
        )
        return jsonify({"question": {'text': question.data[0]['question_text'], 'id': question.data[0]['question_id']}}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "upload failed"}), 500

@app.route('/api/get_submissions', methods=['POST'])
def get_submissions():
    try:
        data = request.get_json()
        question_id = data.get('question_id')
        response = (
            supabase.table('responses').select('*').eq('question_id', question_id).execute()
        )
        responses = {r['response_id']: r['response_text'] for r in response.data}
        return jsonify(responses)
    except Exception as e:
        print(e)
        return jsonify({"error": "failed to fetch question"}), 500
    
@app.route('/api/submit', methods=['POST'])
def submit():
    data = request.get_json()
    session_id = data.get('session_id')
    student_id = data.get('user_id')
    text = data.get('text')
    try:
        session = (
            supabase.table('sessions').select('*').eq('session_id', session_id).execute()
        )
        question_id = session.data[0]['current_question']
        response = (
            supabase.table('responses').insert({
                'question_id': question_id,
                'student_id': student_id,
                'response_text': text
            }).execute()
        )
        return jsonify(response.data), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "failed to fetch from database"}), 500

if __name__ == '__main__':
    app.run(debug=True) 