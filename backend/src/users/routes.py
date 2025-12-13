from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import users_bp
from .repository import UserRepository

@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()
    user = UserRepository.get_by_id(current_user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
        
    return jsonify(user.to_dict()), 200