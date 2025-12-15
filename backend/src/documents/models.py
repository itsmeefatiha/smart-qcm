from src.extensions import db
from datetime import datetime

class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    
    # Metadata for Organization
    filename = db.Column(db.String(255), nullable=False)
    module = db.Column(db.String(100), nullable=False)    # e.g., "Analyse de Données"
    branch = db.Column(db.String(100), nullable=True)     # e.g., "Génie Logiciel"
    year = db.Column(db.String(20), nullable=True)        # e.g., "2024-2025"
    
    # Storage
    file_path = db.Column(db.String(500), nullable=False) # Physical path on disk
    
    # THE AI GOLD MINE: We store the full text here
    # Postgres TEXT type can hold ~1GB of text, plenty for large courses.
    extracted_text = db.Column(db.Text, nullable=True)
    
    # Archival & History
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_archived = db.Column(db.Boolean, default=False)
    
    # Foreign Key (Who uploaded it?)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "filename": self.filename,
            "module": self.module,
            "branch": self.branch,
            "year": self.year,
            "upload_date": self.upload_date.isoformat(),
            "has_text": bool(self.extracted_text), # Just a flag for UI
            "preview": self.extracted_text[:100] + "..." if self.extracted_text else ""
        }