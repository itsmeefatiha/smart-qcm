from src.extensions import db
from datetime import datetime

class QCM(db.Model):
    __tablename__ = 'qcm'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, default="Nouveau QCM")
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)

    # A QCM is generated from a Document
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=False)
    # A QCM is created by a User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationships
    document = db.relationship('Document', backref=db.backref('qcms', lazy=True))
    user = db.relationship('User', backref=db.backref('qcms', lazy=True))
    questions = db.relationship('Question', back_populates='qcm', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "creation_date": self.creation_date.isoformat(),
            "document_id": self.document_id,
            "user_id": self.user_id,
            "questions": [question.to_dict() for question in self.questions]
        }


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)

    # A Question belongs to a QCM
    qcm_id = db.Column(db.Integer, db.ForeignKey('qcm.id'), nullable=False)

    # Relationships
    qcm = db.relationship('QCM', back_populates='questions')
    choices = db.relationship('Choice', back_populates='question', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "choices": [choice.to_dict() for choice in self.choices]
        }


class Choice(db.Model):
    __tablename__ = 'choices'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, default=False, nullable=False)

    # A Choice belongs to a Question
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)

    # Relationships
    question = db.relationship('Question', back_populates='choices')

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "is_correct": self.is_correct
        }
