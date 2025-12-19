import datetime
from src.extensions import db
from .models import ExamSession, StudentAttempt, StudentAnswer
import random
import string

class ExamRepository:
    @staticmethod
    def generate_code():
        """Generates a random 6-character code like 'A7X92Z'"""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    @staticmethod
    def create_session(data):
        session = ExamSession(
            code=ExamRepository.generate_code(),
            start_time=data['start_time'],
            end_time=data['end_time'],
            duration_minutes=data['duration_minutes'],
            total_grade=data['total_grade'], # <--- Added this
            qcm_id=data['qcm_id'],
            professor_id=data['professor_id']
        )
        db.session.add(session)
        db.session.commit()
        return session

    @staticmethod
    def get_session_by_id(session_id):
        return ExamSession.query.get(session_id)

    @staticmethod
    def get_session_by_code(code):
        return ExamSession.query.filter_by(code=code, is_active=True).first()

    @staticmethod
    def create_attempt(user_id, session_id):
        attempt = StudentAttempt(user_id=user_id, session_id=session_id)
        db.session.add(attempt)
        db.session.commit()
        return attempt

    @staticmethod
    def get_attempt(attempt_id):
        return StudentAttempt.query.get(attempt_id)
    
    @staticmethod
    def save_answers_and_score(attempt, answers_list, total_score):
        # 1. Save all answers
        for ans in answers_list:
            db.session.add(ans)
        
        # 2. Update Attempt status
        attempt.score = total_score
        attempt.finished_at = datetime.utcnow()
        
        db.session.commit()

    @staticmethod
    def get_student_attempt(user_id, session_id):
        return StudentAttempt.query.filter_by(user_id=user_id, session_id=session_id).first()