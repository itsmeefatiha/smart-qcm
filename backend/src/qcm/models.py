from src.extensions import db
from datetime import datetime

class QCM(db.Model):
    __tablename__ = 'qcms'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    level = db.Column(db.String(50), nullable=False) # e.g., "Easy", "Hard"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=False)
    document = db.relationship('Document', backref='qcms', lazy=True)
    
    # One QCM has many Questions
    questions = db.relationship('Question', backref='qcm', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "level": self.level,
            "created_at": self.created_at.isoformat(),
            "question_count": len(self.questions),
            "questions": [q.to_dict() for q in self.questions] 
        }

class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    
    # Store choices as JSON: [{"text": "A", "is_correct": false}, ...]
    choices = db.Column(db.JSON, nullable=False) 
    
    qcm_id = db.Column(db.Integer, db.ForeignKey('qcms.id'), nullable=False)
    duration = db.Column(db.Integer, default=30) # Duration in seconds

    def get_correct_choice_index(self):
        """Helper to find which index (0, 1, 2, 3) is the correct one"""
        if not self.choices:
            return -1
        for index, choice in enumerate(self.choices):
            if choice.get('is_correct'):
                return index
        return -1

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "choices": self.choices
        }