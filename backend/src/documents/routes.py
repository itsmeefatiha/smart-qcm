from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import documents_bp
from .service import DocumentService

@documents_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload():
    """
    Upload a course document (PDF/DOCX).
    Expects 'file' and form-data: module, branch, year.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
        
    file = request.files['file']
    user_id = get_jwt_identity()
    
    # Pass request.form because data comes as multipart/form-data
    doc, error = DocumentService.upload_document(file, request.form, user_id)
    
    if error:
        return jsonify({"error": error}), 400
        
    return jsonify({
        "message": "Document processed successfully", 
        "document": doc.to_dict()
    }), 201

@documents_bp.route('/', methods=['GET'])
@jwt_required()
def list_documents():
    """History of uploaded documents"""
    user_id = get_jwt_identity()
    docs = DocumentService.get_user_documents(user_id)
    return jsonify([d.to_dict() for d in docs]), 200