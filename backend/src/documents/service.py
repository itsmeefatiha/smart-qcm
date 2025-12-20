import os
from werkzeug.utils import secure_filename
from .extractor import extract_text_from_file, allowed_file
from .repository import DocumentRepository
from .models import Document
from src.users.models import User, UserRole # Need this to check roles

UPLOAD_DIR = os.path.join(os.getcwd(), 'uploads')
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

class DocumentService:
    @staticmethod
    def upload_document(file, data, user_id):
        # 1. Validation
        if not file or not allowed_file(file.filename):
            return None, "Invalid file format."

        # CHECK BRANCH ID
        branch_id = data.get('branch_id')
        if not branch_id:
            return None, "Branch ID is required."

        # 2. Secure Save
        filename = secure_filename(file.filename)
        save_name = f"{user_id}_{filename}" 
        file_path = os.path.join(UPLOAD_DIR, save_name)
        
        try:
            file.save(file_path)
            
            # 3. Text Extraction
            extracted_text = extract_text_from_file(file_path) or ""
            
            # 4. Create Record with Foreign Key
            new_doc = Document(
                filename=filename,
                file_path=file_path,
                module=data.get('module', 'General'),
                year=data.get('year', ''),
                extracted_text=extracted_text,
                user_id=user_id,
                branch_id=branch_id # <--- Saving the ID
            )
            
            return DocumentRepository.create(new_doc), None

        except Exception as e:
            return None, str(e)

    @staticmethod
    def get_documents_for_user(user_id):
        """
        Smart Listing Logic:
        - Students -> See documents for their BRANCH.
        - Professors -> See documents THEY uploaded.
        """
        user = User.query.get(user_id)
        if not user:
            return []

        if user.role == UserRole.STUDENT:
            # SAFETY CHECK: If student has no branch, they see nothing
            if not user.branch_id:
                return []
            return DocumentRepository.get_by_branch(user.branch_id)
        
        else:
            # Professors/Managers see what they created
            return DocumentRepository.get_by_uploader(user_id)