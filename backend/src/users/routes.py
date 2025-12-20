from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from src.auth.decorators import role_required
from src.auth.schemas import RegisterSchema
from src.users.models import UserRole
from src.users.service import UserService
from . import users_bp
from .repository import UserRepository

@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()
    user = UserRepository.get_by_id(int(current_user_id))
    
    if not user:
        return jsonify({"error": "User not found"}), 404
        
    return jsonify(user.to_dict()), 200

@users_bp.route('/profile/image', methods=['POST'])
@jwt_required()
def upload_profile_image():
    user_id = get_jwt_identity()
    
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
        
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    # Check Allowed Extensions (Optional but recommended)
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    if '.' not in file.filename or \
       file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
        return jsonify({"error": "File type not allowed"}), 400

    filename, error = UserService.save_profile_picture(user_id, file)
    
    if error:
        return jsonify({"error": error}), 500
        
    return jsonify({
        "message": "Profile image updated", 
        "image_url": f"http://localhost:5000/static/profile_pics/{filename}"
    }), 200

@users_bp.route('/', methods=['POST'])
@role_required([UserRole.ADMIN])
def create_user_by_admin():
    """
    Admin Endpoint: Create any user (Manager, Prof, Student).
    The user will be ACTIVE immediately.
    """
    data = request.get_json()

    # 1. Reuse the Auth Schema for validation (Checks password strength, email format)
    schema = RegisterSchema()
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        return jsonify({"error": "Validation Failed", "messages": err.messages}), 400

    # 2. Create User (Pass is_active=True)
    user, error = UserService.create_user(validated_data, is_active=True)

    if error:
        return jsonify({"error": error}), 400

    return jsonify({
        "message": "User created successfully by Admin",
        "user": user.to_dict()
    }), 201

@users_bp.route('/', methods=['GET'])
@role_required([UserRole.ADMIN])
def list_all_users():
    """
    Admin Endpoint: List all registered users.
    """
    # Note: You might want to add pagination later if you have 1000s of users
    from src.users.models import User
    users = User.query.all()
    
    return jsonify([u.to_dict() for u in users]), 200

@users_bp.route('/<int:user_id>', methods=['DELETE'])
@role_required([UserRole.ADMIN])
def delete_user(user_id):
    """
    Admin Endpoint: Delete a user.
    """
    from src.extensions import db
    from src.users.models import User
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
        
    # Prevent Admin from deleting themselves
    current_admin_id = int(get_jwt_identity())
    if user.id == current_admin_id:
        return jsonify({"error": "You cannot delete your own account"}), 403

    db.session.delete(user)
    db.session.commit()
    
    return jsonify({"message": "User deleted successfully"}), 200