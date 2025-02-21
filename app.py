from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask API!"})

@app.route('/api/test')
def test():
    return jsonify({"message": "API is working!"})

# Store questions in memory (in production, use a proper database)
questions = []

@app.route('/api/questions', methods=['GET', 'POST'])
def handle_questions():
    if request.method == 'POST':
        # Get the questions from the request body
        new_questions = request.get_json()
        if not isinstance(new_questions, list):
            return jsonify({"error": "Expected a list of questions"}), 400
        
        # Add the questions to our storage
        questions.extend(new_questions)
        print(questions)
        return jsonify({"message": "Questions added successfully", "count": len(new_questions)}), 201
    
    # Handle GET request
    return jsonify({"questions": questions})


if __name__ == '__main__':
    app.run(debug=True) 