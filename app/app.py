from flask import Flask
from flask_cors import CORS
from routes.session_routes import session_bp
from routes.question_routes import question_bp
from routes.main_routes import main_bp
from models.session import SessionManager

app = Flask(__name__)
session_manager = SessionManager()

CORS(app, 
     origins=["http://localhost:5173", "http://127.0.0.1:3000", "http://10.27.128.109:5173"],  # Specify your frontend origin
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
     allow_headers=["Content-Type", "Authorization"],
     supports_credentials=True)

# CORS(app, 
#      resources={r"/api/*": {  # Apply to all /api/ routes
#          "origins": ["http://localhost:5173", "http://127.0.0.1:3000"],
#          "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
#          "allow_headers": ["Content-Type", "Authorization"],
#          "supports_credentials": True
#      }},
#      expose_headers=["Content-Range", "X-Content-Range"]
# )

# Register blueprints
app.register_blueprint(main_bp)
app.register_blueprint(session_bp, url_prefix='/api/session')
app.register_blueprint(question_bp, url_prefix='/api/questions')

# Pass session_manager to blueprints
session_bp.session_manager = session_manager
question_bp.session_manager = session_manager

if __name__ == '__main__':
    app.run(debug=True)

# session_manager = SessionManager()

# @app.route('/')
# def home():
#     return jsonify({"message": "Welcome to the Flask API!"})

# @app.route('/api/test')
# def test():
#     return jsonify({"message": "API is working!"})

# @app.route('/api/questions', methods=['GET', 'POST'])
# def handle_questions():
#     if request.method == 'POST':
#         new_questions = request.get_json()
#         if not isinstance(new_questions, list):
#             return jsonify({"error": "Expected a list of questions"}), 400
        
#         # Format questions if they're not already in the correct format
#         formatted_questions = [
#             {'text': q} if isinstance(q, str) else q 
#             for q in new_questions
#         ]
        
#         # Create a new session with these questions
#         # session_id = datetime.now().strftime("%Y%m%d-%H%M%S")
#         session_id = "awesome-tiger" # testing
#         session_manager.create_session(session_id, formatted_questions)
        
#         return jsonify({
#             "message": "Questions added successfully",
#             "sessionId": session_id,
#             "count": len(formatted_questions)
#         }), 201
    
#     # Handle GET request
#     latest_session = next(iter(session_manager.sessions.values()), None)
#     questions = []
#     if latest_session:
#         # Ensure consistent format with frontend Question interface
#         questions = [
#             q if isinstance(q, dict) else {'text': q} 
#             for q in latest_session.questions
#         ]
#     return jsonify({"questions": questions})

# def parse_txt(file_content):
#     text = file_content.decode('utf-8')
#     return [line.strip() for line in text.split('\n') if line.strip()]

# def parse_docx(file_content):
#     doc = Document(io.BytesIO(file_content))
#     return [paragraph.text.strip() for paragraph in doc.paragraphs if paragraph.text.strip()]

# def parse_pdf(file_content):
#     pdf_file = io.BytesIO(file_content)
#     reader = PyPDF2.PdfReader(pdf_file)
#     questions = []
#     full_text = ""
    
#     # First combine all text from all pages
#     for page in reader.pages:
#         full_text += page.extract_text() + " "
    
#     # Split by question marks to identify questions
#     potential_questions = full_text.split('?')
    
#     for q in potential_questions:
#         # Clean up the question
#         cleaned = q.strip()
#         # Skip if empty or too short
#         if not cleaned or len(cleaned) < 5:  
#             continue
            
#         # Add back the question mark if it's not the last segment
#         # (last segment won't be a question since it's after the last question mark)
#         if q != potential_questions[-1]:
#             cleaned += '?'
            
#         # Look for common question starters
#         question_starters = ['what', 'why', 'how', 'where', 'when', 'who', 'which', 'whose', 'whom']
#         words = cleaned.lower().split()
        
#         # Add if it starts with a question word or already has a question mark
#         if (words and words[0] in question_starters) or '?' in cleaned:
#             questions.append(cleaned)
            
#     return questions

# @app.route('/api/questions/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file provided'}), 400
    
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'No file selected'}), 400

#     try:
#         file_content = file.read()
#         file_extension = file.filename.split('.')[-1].lower()
        
#         if file_extension == 'txt':
#             questions = parse_txt(file_content)
#         elif file_extension == 'docx':
#             questions = parse_docx(file_content)
#         elif file_extension == 'pdf':
#             questions = parse_pdf(file_content)
#         else:
#             return jsonify({'error': 'Unsupported file type'}), 400

#         # Format questions to match frontend interface
#         formatted_questions = [{'text': q} for q in questions]
        
#         # Create a new session with the extracted questions
#         # session_id = datetime.now().strftime("%Y%m%d-%H%M%S")
#         session_id = "awesome-tiger" # testing
#         session_manager.create_session(session_id, formatted_questions)

#         return jsonify({
#             'message': 'File processed successfully',
#             'sessionId': session_id,
#             'questions': formatted_questions
#         })

#     except Exception as e:
#         return jsonify({'error': f'Error processing file: {str(e)}'}), 500

# @app.route('/api/session/<session_id>/current-question', methods=['GET'])
# def get_current_question(session_id):
#     print(session_id)
#     session = session_manager.sessions.get(session_id)
#     print(session)
#     if not session or session.current_question_index is None:
#         return jsonify({'error': 'No active question'}), 404
    
#     # Ensure question format matches frontend interface
#     question = session.questions[session.current_question_index]
#     if isinstance(question, str):
#         question = {'text': question}
    
#     print(question)
#     return jsonify({
#         'text': question['text'],
#         'questionIndex': session.current_question_index
#     })

# @app.route('/api/session/<session_id>/set-question', methods=['POST'])
# def set_current_question(session_id):
#     data = request.json
#     question_index = data.get('questionIndex')
    
#     if question_index is None:
#         return jsonify({'error': 'questionIndex is required'}), 400
    
#     success = session_manager.set_current_question(session_id, question_index)
#     if not success:
#         return jsonify({'error': 'Session not found'}), 404
    
#     return jsonify({'message': 'Question updated successfully'})

# @app.route('/api/session/<session_id>/submit', methods=['POST'])
# def submit_answer(session_id):
#     data = request.json
#     student_id = data.get('studentId')
#     submission = data.get('submission')
#     question_index = data.get('questionIndex')
    
#     if not all([student_id, submission, question_index is not None]):
#         return jsonify({'error': 'Missing required fields'}), 400
    
#     success = session_manager.submit_answer(
#         session_id, question_index, student_id, submission
#     )
#     if not success:
#         return jsonify({'error': 'Submission failed'}), 400
    
#     return jsonify({'message': 'Submission received'})

# @app.route('/api/session/<session_id>/submissions', methods=['GET'])
# def get_submissions(session_id):
#     session = session_manager.sessions.get(session_id)
#     if not session:
#         return jsonify({'error': 'Session not found'}), 404
    
#     current_index = session.current_question_index
#     if current_index is None:
#         return jsonify({'submissions': []})
    
#     return jsonify({
#         'submissions': session.submissions.get(current_index, {})
#     })

# if __name__ == '__main__':
#     app.run(debug=True) 