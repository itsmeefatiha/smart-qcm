import fitz  # PyMuPDF
import docx
import os

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_file(file_path):
    """
    Detects file type and extracts text using the most efficient library.
    Returns: Cleaned string ready for AI processing.
    """
    ext = file_path.rsplit('.', 1)[1].lower()
    
    try:
        if ext == 'pdf':
            return _read_pdf(file_path)
        elif ext == 'docx':
            return _read_docx(file_path)
        elif ext == 'txt':
            return _read_txt(file_path)
    except Exception as e:
        print(f"Extraction Error: {str(e)}")
        return ""

def _read_pdf(path):
    text = ""
    with fitz.open(path) as doc:
        for page in doc:
            # "text" mode is fast and preserves natural reading order
            text += page.get_text("text") + "\n"
    return _clean_text(text)

def _read_docx(path):
    doc = docx.Document(path)
    # Join paragraphs with newlines
    text = "\n".join([para.text for para in doc.paragraphs])
    return _clean_text(text)

def _read_txt(path):
    with open(path, 'r', encoding='utf-8') as f:
        return _clean_text(f.read())

def _clean_text(text):
    """
    Basic cleanup to help the AI (removes excessive whitespace).
    """
    # Replace multiple newlines with a single one to save token space
    return "\n".join([line.strip() for line in text.splitlines() if line.strip()])