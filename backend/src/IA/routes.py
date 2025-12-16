from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import ia_bp
from .service import QCMService

@ia_bp.route('/generate', methods=['POST'])
@jwt_required()
def generate_qcm():
    """
    Déclenche la génération d'un QCM pour un document donné.
    Expects JSON: {"document_id": int, "num_questions": int (optional, default 5)}
    """
    data = request.get_json()
    document_id = data.get('document_id')
    num_questions = data.get('num_questions', 5)
    user_id = get_jwt_identity()
    
    if not document_id:
        return jsonify({"error": "document_id manquant."}), 400
        
    if num_questions < 1:
        return jsonify({"error": "Le nombre de questions doit être positif."}), 400

    qcm, error = QCMService.generate_and_save_qcm(
        document_id=document_id, 
        user_id=user_id, 
        num_questions=num_questions
    )
    
    if error:
        return jsonify({"error": error}), 400
        
    return jsonify({
        "message": "QCM généré et sauvegardé avec succès.", 
        "qcm": qcm.to_dict()
    }), 201

@ia_bp.route('/', methods=['GET'])
@jwt_required()
def list_qcms():
    """Liste tous les QCM générés par l'utilisateur courant."""
    user_id = get_jwt_identity()
    qcms = QCMService.get_user_qcms(user_id)
    return jsonify([q.to_dict() for q in qcms]), 200

@ia_bp.route('/<int:qcm_id>', methods=['GET'])
@jwt_required()
def get_qcm_details(qcm_id):
    """Affiche les détails d'un QCM, y compris les questions et les choix."""
    qcm = QCMService.get_qcm(qcm_id)
    
    if not qcm:
        return jsonify({"error": "QCM introuvable."}), 404

    # Vérification d'appartenance (facultatif mais recommandé pour la sécurité)
    if qcm.user_id != get_jwt_identity():
         return jsonify({"error": "Accès non autorisé."}), 403

    return jsonify({
        "id": qcm.id,
        "title": qcm.title,
        "document_id": qcm.document_id,
        "questions": [q.to_dict() for q in qcm.questions.all()]
    }), 200