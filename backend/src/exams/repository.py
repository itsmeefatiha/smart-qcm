from datetime import datetime
from src.extensions import db
from .models import ExamSession, StudentAttempt, StudentAnswer
import random
import string

class ExamRepository:
    @staticmethod
    def generate_code():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    @staticmethod
    def create_session(data):
        # We now accept 'end_time' which is calculated by the Service, not the User
        session = ExamSession(
            code=ExamRepository.generate_code(),
            description=data.get('description', ''),
            start_time=data['start_time'],
            end_time=data['end_time'],
            duration_minutes=data['duration_minutes'],
            total_grade=data['total_grade'],
            qcm_id=data['qcm_id'],
            professor_id=data['professor_id'],
            branch_id=data['branch_id']
        )
        db.session.add(session)
        db.session.commit()
        return session

    @staticmethod
    def delete_session(session):
        db.session.delete(session)
        db.session.commit()

    @staticmethod
    def get_all_by_professor(professor_id):
        """Returns ALL exams (active & finished) for the professor"""
        return ExamSession.query.filter_by(professor_id=professor_id).order_by(ExamSession.start_time.desc()).all()

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
        attempt.finished_at = datetime.now()
        
        db.session.commit()

    @staticmethod
    def get_student_attempt(user_id, session_id):
        return StudentAttempt.query.filter_by(user_id=user_id, session_id=session_id).first()
    
    @staticmethod
    def get_all_exams():
        """Returns every single exam session in the database"""
        return ExamSession.query.order_by(ExamSession.start_time.desc()).all()
    
    @staticmethod
    def save_individual_answer(attempt_id, question_id, selected_index):
        """Save or update a single answer for a question"""
        # Check if answer already exists
        existing_answer = StudentAnswer.query.filter_by(
            attempt_id=attempt_id,
            question_id=question_id
        ).first()
        
        if existing_answer:
            # Update existing answer
            existing_answer.selected_choice_index = selected_index
        else:
            # Create new answer
            new_answer = StudentAnswer(
                attempt_id=attempt_id,
                question_id=question_id,
                selected_choice_index=selected_index,
                is_correct=False  # Will be calculated on final submission
            )
            db.session.add(new_answer)
        
        db.session.commit()
        return existing_answer if existing_answer else new_answer
    
    @staticmethod
    def get_saved_answers(attempt_id):
        """Get all saved answers for an attempt"""
        return StudentAnswer.query.filter_by(attempt_id=attempt_id).all()