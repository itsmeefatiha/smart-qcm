from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from .service import QCMService
from . import qcm_bp

@qcm_bp.route('/generate', methods=['POST'])
@jwt_required()
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

@qcm_bp.route('/<int:qcm_id>', methods=['GET'])
@jwt_required()
def get_qcm(qcm_id):
    """Returns the QCM with all its questions"""
    qcm = QCMService.get_exam_details(qcm_id)
    if not qcm:
        return jsonify({"error": "Exam not found"}), 404
        
    return jsonify({
        "id": qcm.id,
        "title": qcm.title,
        "questions": [q.to_dict() for q in qcm.questions]
    }), 200