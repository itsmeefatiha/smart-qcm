from src.documents.repository import DocumentRepository
from .repository import QCMRepository
from .ai_generation import AIGenerator

class QCMService:
    @staticmethod
    def generate_exam(user_id, doc_id, num_questions, level):
        # 1. Fetch the source text from the database
        document = DocumentRepository.get_by_id(doc_id)
        
        if not document:
            return None, "Document not found."
        
        if not document.extracted_text:
            return None, "This document has no text. AI cannot read it."

        # 2. Call Gemini AI
        questions_json, error = AIGenerator.generate(
            text_content=document.extracted_text, 
            num_questions=num_questions, 
            level=level
        )
        
        if error:
            return None, error

        # 3. Save to Database
        qcm_data = {
            "title": f"Exam: {document.module} ({level})",
            "level": level,
            "user_id": user_id,
            "document_id": doc_id
        }
        
        try:
            qcm = QCMRepository.create_qcm_with_questions(qcm_data, questions_json)
            return qcm, None
        except Exception as e:
            return None, f"Database Error: {str(e)}"

    @staticmethod
    def get_exam_details(qcm_id):
        return QCMRepository.get_by_id(qcm_id)