from src.extensions import db
from .models import Document

class DocumentRepository:
    @staticmethod
    def create(doc):
        db.session.add(doc)
        db.session.commit()
        return doc

    @staticmethod
    def get_by_id(doc_id):
        return Document.query.get(doc_id)

    @staticmethod
    def get_all_by_user(user_id):
        return Document.query.filter_by(user_id=user_id, is_archived=False).order_by(Document.upload_date.desc()).all()

    @staticmethod
    def archive(doc_id):
        doc = Document.query.get(doc_id)
        if doc:
            doc.is_archived = True
            db.session.commit()
            return True
        return False