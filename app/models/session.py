from datetime import datetime

class Session:
    def __init__(self, session_id, questions):
        self.session_id = session_id
        self.questions = questions 
        self.current_question_index = 0
        self.submissions = {}  # Format: {question_index: {student_id: submission}}
        self.active = True
        self.created_at = datetime.now()

class SessionManager:
    def __init__(self):
        self.sessions = {}  # Format: {session_id: Session}

    def create_session(self, session_id, questions):
        # TODO: should probably generate the session id with a fun random slug 
        self.sessions[session_id] = Session(session_id, questions)
        return session_id

    def set_current_question(self, session_id, question_index):
        session = self.sessions.get(session_id)
        if session:
            session.current_question_index = question_index
            return True
        return False

    def submit_answer(self, session_id, question_index, student_id, submission):
        session = self.sessions.get(session_id)
        if not session:
            return False
        
        if question_index not in session.submissions:
            session.submissions[question_index] = {}
        
        session.submissions[question_index][student_id] = {
            'text': submission,
            'timestamp': datetime.now()
        }
        return True