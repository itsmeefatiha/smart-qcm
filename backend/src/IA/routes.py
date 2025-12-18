
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.extensions import db
from .schemas import QCMRequest, QCMResponse
from .service import generate_qcm
from .models import QCM, Question, Choice
from src.documents.models import Document
from . import ia_bp

@ia_bp.route('/generate_qcm', methods=['POST'])
@jwt_required()
def generate_qcm_endpoint():
    data = request.get_json()
    user_id = int(get_jwt_identity())
    
    document_id = data.get('document_id')
    if not document_id:
        return jsonify({"error": "document_id required"}), 400
    
    document = Document.query.get(document_id)
    if not document or document.user_id != user_id:
        return jsonify({"error": "Document not found or access denied"}), 404
    
    text = document.extracted_text
    if not text:
        return jsonify({"error": "No text extracted from document"}), 400
    
    role = data.get('role')
    difficulty = data.get('difficulty')
    
    questions = generate_qcm(
        text=text,
        role=role,
        difficulty=difficulty
    )
    # Save to DB
    qcm = QCM(document_id=document_id, user_id=user_id)
    db.session.add(qcm)
    db.session.flush()
    for q in questions:
        question = Question(text=q.text, qcm_id=qcm.id)
        db.session.add(question)
        db.session.flush()
        for c in q.choices:
            choice = Choice(text=c.text, is_correct=c.is_correct, question_id=question.id)
            db.session.add(choice)
    db.session.commit()
    qcm_id = qcm.id
    response = QCMResponse(qcm_id=qcm_id, questions=questions)
    return jsonify(response.dict())
