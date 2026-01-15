from src.extensions import db
from datetime import datetime

class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    
    # Metadata
    filename = db.Column(db.String(255), nullable=False)
    module = db.Column(db.String(100), nullable=False)    # e.g., "Analyse de Données"
    year = db.Column(db.String(20), nullable=True)        # e.g., "2024-2025"
    
    # Was: branch = db.Column(db.String(100)...)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=False)
    
    # Storage
    file_path = db.Column(db.String(500), nullable=False)
    extracted_text = db.Column(db.Text, nullable=True)
    
    # Archival & History
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_archived = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationships
    # Access the branch name via self.branch.name
    # (The backref 'documents' was already defined in Branch model, so we don't strictly need to redefine it here, 
    # but defining the relationship here makes access easier if backref wasn't explicit)
    # branch = db.relationship('Branch', backref='documents') # optional if backref exists
    branch = db.relationship('Branch', backref='documents')

    def to_dict(self):
        return {
            "id": self.id,
            "filename": self.filename,
            "module": self.module,
            # Fetch name dynamically from the relationship
            "branch": self.branch.name if self.branch else "Unknown",
            "year": self.year,
            "upload_date": self.upload_date.isoformat(),
            "preview": self.extracted_text[:100] + "..." if self.extracted_text else ""
        }