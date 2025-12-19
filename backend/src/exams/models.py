from src.extensions import db
from datetime import datetime

class ExamSession(db.Model):
    """
    Represents a 'Live' instance of a QCM that students can join.
    """
    __tablename__ = 'exam_sessions'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False) # e.g. "X7Y-22A"
    
    start_time = db.Column(db.DateTime, nullable=False) # When the exam opens
    end_time = db.Column(db.DateTime, nullable=False)   # When the exam closes
    duration_minutes = db.Column(db.Integer, nullable=False) # Time allowed (e.g. 60 mins)
    
    is_active = db.Column(db.Boolean, default=True)

    # Relationships
    qcm_id = db.Column(db.Integer, db.ForeignKey('qcms.id'), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    attempts = db.relationship('StudentAttempt', backref='session', lazy=True)

class StudentAttempt(db.Model):
    """
    Tracks one student taking one exam.
    """
    __tablename__ = 'student_attempts'

    id = db.Column(db.Integer, primary_key=True)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    finished_at = db.Column(db.DateTime, nullable=True)
    
    score = db.Column(db.Float, default=0.0) # The final calculated grade
    
    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('exam_sessions.id'), nullable=False)
    
    answers = db.relationship('StudentAnswer', backref='attempt', lazy=True)

class StudentAnswer(db.Model):
    """
    Stores exactly what the student clicked for each question.
    """
    __tablename__ = 'student_answers'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    attempt_id = db.Column(db.Integer, db.ForeignKey('student_attempts.id'), nullable=False)
    
    selected_choice_index = db.Column(db.Integer, nullable=False) # 0, 1, 2, or 3
    is_correct = db.Column(db.Boolean, default=False) # Calculated at submission