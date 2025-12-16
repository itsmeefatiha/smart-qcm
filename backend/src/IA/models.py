from src.extensions import db
from datetime import datetime

class QCM(db.Model):
    __tablename__ = 'qcm'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    # Référence au document source
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=False)
    # L'utilisateur qui a généré le QCM
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    generation_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relation avec les questions
    questions = db.relationship('Question', backref='qcm', lazy='dynamic', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "document_id": self.document_id,
            "generation_date": self.generation_date.isoformat(),
            "questions_count": self.questions.count()
        }

class Question(db.Model):
    __tablename__ = 'question'
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    
    # Référence au QCM parent
    qcm_id = db.Column(db.Integer, db.ForeignKey('qcm.id'), nullable=False)
    
    # Relation avec les choix
    choix = db.relationship('Choix', backref='question', lazy='dynamic', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "choix": [c.to_dict() for c in self.choix.all()]
        }

class Choix(db.Model):
    __tablename__ = 'choix'
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    
    # Référence à la Question parente
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "is_correct": self.is_correct # Peut être omis pour l'utilisateur final
        }