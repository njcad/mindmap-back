from flask import Blueprint, jsonify, request
from utils.utils import parse_txt, parse_docx, parse_pdf

# note that this blueprint is passed the session_manager object from the app.py file
question_bp = Blueprint('questions', __name__)


@question_bp.route('', methods=['GET', 'POST'])
def handle_questions():
    if request.method == 'POST':
        new_questions = request.get_json()
        if not isinstance(new_questions, list):
            return jsonify({"error": "Expected a list of questions"}), 400
        
        formatted_questions = [
            {'text': q} if isinstance(q, str) else q 
            for q in new_questions
        ]
        
        session_id = "awesome-tiger" # testing
        question_bp.session_manager.create_session(session_id, formatted_questions)
        
        return jsonify({
            "message": "Questions added successfully",
            "sessionId": session_id,
            "count": len(formatted_questions)
        }), 201
    
    latest_session = next(iter(question_bp.session_manager.sessions.values()), None)
    questions = []
    if latest_session:
        questions = [
            q if isinstance(q, dict) else {'text': q} 
            for q in latest_session.questions
        ]
    return jsonify({"questions": questions})

@question_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    try:
        file_content = file.read()
        file_extension = file.filename.split('.')[-1].lower()
        
        if file_extension == 'txt':
            questions = parse_txt(file_content)
        elif file_extension == 'docx':
            questions = parse_docx(file_content)
        elif file_extension == 'pdf':
            questions = parse_pdf(file_content)
        else:
            return jsonify({'error': 'Unsupported file type'}), 400

        formatted_questions = [{'text': q} for q in questions]
        session_id = "awesome-tiger" # testing
        question_bp.session_manager.create_session(session_id, formatted_questions)

        return jsonify({
            'message': 'File processed successfully',
            'sessionId': session_id,
            'questions': formatted_questions
        })

    except Exception as e:
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500