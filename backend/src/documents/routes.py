from flask import request, jsonify
from flasgger import swag_from
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import documents_bp
from .service import DocumentService

@documents_bp.route('/upload', methods=['POST'])
@jwt_required()
@swag_from({
    'tags': ['Documents'],
    'summary': 'Upload and process a document',
    'consumes': ['multipart/form-data'],
    'security': [{'BearerAuth': []}],
    'parameters': [{
        'in': 'formData',
        'name': 'file',
        'type': 'file',
        'required': True,
    }, {
        'in': 'formData',
        'name': 'branch_id',
        'type': 'integer',
        'required': False,
    }, {
        'in': 'formData',
        'name': 'module',
        'type': 'string',
        'required': False,
    }],
    'responses': {
        201: {'description': 'Document processed'},
        400: {'description': 'Validation or processing error'},
    },
})
def upload():
    # Expects form-data: { "file": ..., "branch_id": 1, "module": "Java" }
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
        
    file = request.files['file']
    user_id = get_jwt_identity()
    
    # Pass request.form (contains branch_id)
    doc, error = DocumentService.upload_document(file, request.form, user_id)
    
    if error:
        return jsonify({"error": error}), 400
        
    return jsonify({
        "message": "Document processed", 
        "document": doc.to_dict()
    }), 201

@documents_bp.route('/', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Documents'],
    'summary': 'List documents available to the current user',
    'security': [{'BearerAuth': []}],
    'responses': {
        200: {'description': 'List of documents'},
    },
})
def list_documents():
    """
    Returns the feed of documents relevant to the specific user.
    """
    user_id = get_jwt_identity()
    docs = DocumentService.get_documents_for_user(user_id)
    return jsonify([d.to_dict() for d in docs]), 200