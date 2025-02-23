from flask import Blueprint, jsonify, request

# note that this blueprint is passed the session_manager object from the app.py file
session_bp = Blueprint('session', __name__)


@session_bp.route('/<session_id>/current-question', methods=['GET'])
def get_current_question(session_id):
    session = session_bp.session_manager.sessions.get(session_id)
    if not session or session.current_question_index is None:
        return jsonify({'error': 'No active question'}), 404
    
    question = session.questions[session.current_question_index]
    if isinstance(question, str):
        question = {'text': question}
    
    return jsonify({
        'text': question['text'],
        'questionIndex': session.current_question_index
    })

@session_bp.route('/<session_id>/set-question', methods=['POST'])
def set_current_question(session_id):
    data = request.json
    question_index = data.get('questionIndex')
    
    if question_index is None:
        return jsonify({'error': 'questionIndex is required'}), 400
    
    success = session_bp.session_manager.set_current_question(session_id, question_index)
    if not success:
        return jsonify({'error': 'Session not found'}), 404
    
    return jsonify({'message': 'Question updated successfully'})

@session_bp.route('/<session_id>/submit', methods=['POST'])
def submit_answer(session_id):
    data = request.json
    student_id = data.get('studentId')
    submission = data.get('submission')
    question_index = data.get('questionIndex')
    
    if not all([student_id, submission, question_index is not None]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    success = session_bp.session_manager.submit_answer(
        session_id, question_index, student_id, submission
    )
    if not success:
        return jsonify({'error': 'Submission failed'}), 400
    
    return jsonify({'message': 'Submission received'})

@session_bp.route('/<session_id>/submissions', methods=['GET'])
def get_submissions(session_id):
    session = session_bp.session_manager.sessions.get(session_id)
    if not session:
        return jsonify({'error': 'Session not found'}), 404
    
    current_index = session.current_question_index
    if current_index is None:
        return jsonify({'submissions': []})
    
    return jsonify({
        'submissions': session.submissions.get(current_index, {})
    })