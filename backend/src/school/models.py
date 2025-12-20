from src.extensions import db

class Branch(db.Model):
    __tablename__ = 'branches'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False) # e.g. "Genie Logiciel"
    description = db.Column(db.Text, nullable=True)

    # --- DELETE THESE LINES ---
    # users = db.relationship('User', backref='branch', lazy=True)      <-- DELETE
    # documents = db.relationship('Document', backref='branch', lazy=True) <-- DELETE
    # exam_sessions = db.relationship('ExamSession', backref='branch', lazy=True) <-- DELETE
    
    # Why? Because in User/Document/ExamSession models, you already have:
    # branch = db.relationship('Branch', backref='users') 
    # This backref AUTOMATICALLY creates the relationship on this side.

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }