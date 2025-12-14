import os
from werkzeug.utils import secure_filename
from .extractor import extract_text_from_file, allowed_file
from .repository import DocumentRepository
from .models import Document

# Define where files go. In production, use an ENV variable.
UPLOAD_DIR = os.path.join(os.getcwd(), 'uploads')
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

class DocumentService:
    @staticmethod
    def upload_document(file, data, user_id):
        # 1. Validation
        if not file or not allowed_file(file.filename):
            return None, "Invalid file format. Allowed: PDF, DOCX, TXT"
        
        # 2. Secure Save
        filename = secure_filename(file.filename)
        # Add timestamp to filename to prevent duplicates
        save_name = f"{user_id}_{filename}" 
        file_path = os.path.join(UPLOAD_DIR, save_name)
        
        try:
            file.save(file_path)
            
            # 3. INTELLIGENT EXTRACTION (The Core Value)
            # We extract text NOW so the AI is fast LATER.
            extracted_text = extract_text_from_file(file_path)
            
            if not extracted_text:
                return None, "Could not extract text. File might be empty or a scanned image."

            # 4. Create Record
            new_doc = Document(
                filename=filename,
                file_path=file_path,
                module=data.get('module', 'General'),
                branch=data.get('branch', ''),
                year=data.get('year', ''),
                extracted_text=extracted_text,
                user_id=user_id
            )
            
            return DocumentRepository.create(new_doc), None

        except Exception as e:
            return None, str(e)

    @staticmethod
    def get_user_documents(user_id):
        return DocumentRepository.get_all_by_user(user_id)