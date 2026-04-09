from flask import request, jsonify, url_for
from flasgger import swag_from
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
@swag_from({
    'tags': ['Users'],
    'summary': 'Get current user profile',
    'security': [{'BearerAuth': []}],
    'responses': {
        200: {'description': 'Current user profile'},
        404: {'description': 'User not found'},
    },
})
def get_profile():
    current_user_id = get_jwt_identity()
    user = UserRepository.get_by_id(int(current_user_id))
    
    if not user:
        return jsonify({"error": "User not found"}), 404
        
    return jsonify(user.to_dict()), 200

@users_bp.route('/profile/image', methods=['POST'])
@jwt_required()
@swag_from({
    'tags': ['Users'],
    'summary': 'Upload a profile image',
    'consumes': ['multipart/form-data'],
    'security': [{'BearerAuth': []}],
    'parameters': [{
        'in': 'formData',
        'name': 'file',
        'type': 'file',
        'required': True,
    }],
    'responses': {
        200: {'description': 'Profile image updated'},
        400: {'description': 'No file selected'},
        500: {'description': 'Upload failed'},
    },
})
def upload_profile_image():
    user_id = get_jwt_identity()
    
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
        
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename, error = UserService.save_profile_picture(user_id, file)
    
    if error:
        return jsonify({"error": error}), 500
        
    # --- CRITICAL FIX: Use Dynamic URL ---
    image_url = url_for('static', filename=f'profile_pics/{filename}', _external=True)
    # -------------------------------------

    return jsonify({
        "message": "Profile image updated", 
        "image_url": image_url
    }), 200

@users_bp.route('/', methods=['POST'])
@role_required([UserRole.ADMIN])
@swag_from({
    'tags': ['Users'],
    'summary': 'Create a user as admin',
    'security': [{'BearerAuth': []}],
    'parameters': [{
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'required': ['email', 'password', 'first_name', 'last_name', 'role'],
        },
    }],
    'responses': {
        201: {'description': 'User created successfully'},
        400: {'description': 'Validation error'},
        403: {'description': 'Unauthorized'},
    },
})
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
@role_required([UserRole.ADMIN, UserRole.MANAGER])
@swag_from({
    'tags': ['Users'],
    'summary': 'List all users',
    'security': [{'BearerAuth': []}],
    'responses': {
        200: {'description': 'List of users'},
        403: {'description': 'Unauthorized'},
    },
})
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
@swag_from({
    'tags': ['Users'],
    'summary': 'Delete a user by ID',
    'security': [{'BearerAuth': []}],
    'parameters': [{
        'in': 'path',
        'name': 'user_id',
        'type': 'integer',
        'required': True,
    }],
    'responses': {
        200: {'description': 'User deleted successfully'},
        403: {'description': 'Unauthorized or self-delete blocked'},
        404: {'description': 'User not found'},
    },
})
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