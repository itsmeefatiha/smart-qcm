from flask import request, jsonify, Blueprint, send_file
from flasgger import swag_from
from flask_jwt_extended import jwt_required, get_jwt_identity
from .service import QCMService
from . import qcm_bp

@qcm_bp.route('/generate', methods=['POST'])
@jwt_required()
@swag_from({
    'tags': ['QCM'],
    'summary': 'Generate a QCM from a document',
    'security': [{'BearerAuth': []}],
    'consumes': ['application/json'],
    'parameters': [{
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'required': ['document_id'],
            'properties': {
                'document_id': {'type': 'integer'},
                'num_questions': {'type': 'integer'},
                'level': {'type': 'string'},
            },
        },
    }],
    'responses': {
        201: {'description': 'Exam generated successfully'},
        400: {'description': 'Missing document ID'},
        500: {'description': 'Generation error'},
    },
})
def generate():
    """
    Payload: { "document_id": 1, "num_questions": 10, "level": "hard" }
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    
    doc_id = data.get('document_id')
    num = data.get('num_questions', 5)
    level = data.get('level', 'medium')

    if not doc_id:
        return jsonify({"error": "Document ID is required"}), 400

    qcm, error = QCMService.generate_exam(user_id, doc_id, num, level)

    if error:
        return jsonify({"error": error}), 500

    return jsonify({
        "message": "Exam generated successfully",
        "qcm_id": qcm.id,
        "title": qcm.title
    }), 201

@qcm_bp.route('/', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['QCM'],
    'summary': 'List QCMs for the current user',
    'security': [{'BearerAuth': []}],
    'responses': {
        200: {'description': 'List of QCMs'},
    },
})
def list_qcms():
    """Returns all QCMs for the current user"""
    user_id = get_jwt_identity()
    qcms = QCMService.get_user_qcms(user_id)

    return jsonify([qcm.to_dict() for qcm in qcms]), 200

@qcm_bp.route('/<int:qcm_id>', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['QCM'],
    'summary': 'Get a QCM with its questions',
    'security': [{'BearerAuth': []}],
    'parameters': [{
        'in': 'path',
        'name': 'qcm_id',
        'type': 'integer',
        'required': True,
    }],
    'responses': {
        200: {'description': 'QCM details'},
        404: {'description': 'Exam not found'},
    },
})
def get_qcm(qcm_id):
    """Returns the QCM with all its questions"""
    qcm = QCMService.get_exam_details(qcm_id)
    if not qcm:
        return jsonify({"error": "Exam not found"}), 404

    return jsonify({
        "id": qcm.id,
        "title": qcm.title,
        "level": qcm.level,
        "questions": [q.to_dict() for q in qcm.questions]
    }), 200

# --- NEW: Delete QCM Route ---
@qcm_bp.route('/<int:qcm_id>', methods=['DELETE'])
@jwt_required()
@swag_from({
    'tags': ['QCM'],
    'summary': 'Delete a QCM',
    'security': [{'BearerAuth': []}],
    'parameters': [{
        'in': 'path',
        'name': 'qcm_id',
        'type': 'integer',
        'required': True,
    }],
    'responses': {
        200: {'description': 'QCM deleted successfully'},
        403: {'description': 'Unauthorized'},
    },
})
def delete_qcm(qcm_id):
    """Deletes a QCM and all its questions"""
    user_id = get_jwt_identity()
    message, status = QCMService.delete_exam(user_id, qcm_id)
    
    if status != 200:
        return jsonify({"error": message}), status
        
    return jsonify({"message": message}), 200

# --- NEW: Edit Question Route ---
@qcm_bp.route('/question/<int:question_id>', methods=['PUT'])
@jwt_required()
@swag_from({
    'tags': ['QCM'],
    'summary': 'Update a single question',
    'security': [{'BearerAuth': []}],
    'parameters': [{
        'in': 'path',
        'name': 'question_id',
        'type': 'integer',
        'required': True,
    }, {
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'properties': {
                'text': {'type': 'string'},
                'choices': {'type': 'array'},
            },
        },
    }],
    'responses': {
        200: {'description': 'Question updated successfully'},
        400: {'description': 'Validation error'},
    },
})
def edit_question(question_id):
    """
    Updates a single question's text and choices.
    Payload: {
        "text": "New question text?",
        "choices": [ {"text": "A", "is_correct": true}, ... ]
    }
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    
    result, status = QCMService.update_question(user_id, question_id, data)
    
    if status != 200:
        return jsonify({"error": result}), status
        
    return jsonify({
        "message": "Question updated successfully",
        "question": result.to_dict()
    }), 200

@qcm_bp.route('/<int:qcm_id>/download', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['QCM'],
    'summary': 'Download a QCM as PDF',
    'security': [{'BearerAuth': []}],
    'parameters': [{
        'in': 'path',
        'name': 'qcm_id',
        'type': 'integer',
        'required': True,
    }],
    'responses': {
        200: {'description': 'PDF file'},
        404: {'description': 'PDF generation failed'},
    },
})
def download_qcm_pdf(qcm_id):
    """
    Generates and downloads the PDF for a specific QCM.
    """
    user_id = get_jwt_identity()
    
    pdf_buffer, error = QCMService.download_pdf(user_id, qcm_id)
    
    if error:
        return jsonify({"error": error}), 404
        
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"exam_{qcm_id}.pdf",
        mimetype='application/pdf'
    )