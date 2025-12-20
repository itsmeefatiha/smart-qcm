from src.documents.repository import DocumentRepository
from .repository import QCMRepository
from .ai_generation import AIGenerator
from .pdf_generator import PDFGenerator
from src.users.models import User, UserRole

class QCMService:
    @staticmethod
    def generate_exam(user_id, doc_id, num_questions, level):
        # 1. Fetch document
        document = DocumentRepository.get_by_id(doc_id)
        if not document or not document.extracted_text:
            return None, "Document not found or empty."

        # 2. Determine Mode based on User Role
        user = User.query.get(user_id)
        if not user:
            return None, "User not found"
            
        # Check if the user is a Professor/Admin or a Student
        is_prof = (user.role == UserRole.PROFESSOR or user.role == UserRole.ADMIN)
        mode = "professor" if is_prof else "student"

        # 3. Call AI with the specific MODE
        questions_json, error = AIGenerator.generate(
            text_content=document.extracted_text, 
            num_questions=num_questions, 
            level=level,
            mode=mode 
        )
        
        if error:
            return None, error

        # 4. Save to Database
        # Use different titles so they are easily distinguishable in the list
        prefix = "Exam" if is_prof else "Practice"
        
        qcm_data = {
            "title": f"{prefix}: {document.module} ({level})",
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

    @staticmethod
    def get_user_qcms(user_id):
        return QCMRepository.get_by_user(user_id)
    
    # --- NEW: Delete Logic ---
    @staticmethod
    def delete_exam(user_id, qcm_id):
        qcm = QCMRepository.get_by_id(qcm_id)
        
        if not qcm:
            return "QCM not found", 404
            
        # Security Check: Force int comparison
        if int(qcm.user_id) != int(user_id):
            return "Unauthorized: You do not own this QCM", 403

        # --- NEW CONFLICT CHECK ---
        # The 'sessions' attribute exists because of the relationship in ExamSession model
        if len(qcm.sessions) > 0:
            return "Warning: You have created exams based on this QCM. Delete exams first.", 409
        # --------------------------

        try:
            QCMRepository.delete_qcm(qcm)
            return "QCM deleted successfully", 200
        except Exception as e:
            return str(e), 500

    # --- NEW: Edit Question Logic ---
    @staticmethod
    def update_question(user_id, question_id, data):
        # 1. Get the question
        question = QCMRepository.get_question_by_id(question_id)
        if not question:
            return "Question not found", 404
            
        # 2. Security Check: Force int comparison
        if int(question.qcm.user_id) != int(user_id):
            return "Unauthorized: You do not own this Question", 403

        # --- NEW SAFEGUARD: Prevent editing if used in an exam ---
        # Editing a question while an exam exists changes history/grades!
        if len(question.qcm.sessions) > 0:
            return "Warning: This QCM is used in an Exam Session. You cannot edit questions unless you delete the exams first.", 409
        # ---------------------------------------------------------
            
        # 3. Validate Data
        new_text = data.get('text')
        new_choices = data.get('choices')
        
        if not new_text or not new_choices:
            return "Text and Choices are required", 400
            
        # 4. Perform Update
        try:
            updated_q = QCMRepository.update_question(question_id, new_text, new_choices)
            return updated_q, 200
        except Exception as e:
            return str(e), 500
        

    @staticmethod
    def download_pdf(user_id, qcm_id):
        qcm = QCMRepository.get_by_id(qcm_id)
        
        if not qcm:
            return None, "QCM not found"
            
        # Optional: Security check (Owner only?)
        # if qcm.user_id != user_id:
        #    return None, "Unauthorized"
            
        pdf_buffer = PDFGenerator.create_pdf(qcm)
        return pdf_buffer, None