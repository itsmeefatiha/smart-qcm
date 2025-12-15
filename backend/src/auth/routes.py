from flask import request, jsonify
from . import auth_bp
from .service import AuthService
from .schemas import RegisterSchema, LoginSchema
from marshmallow import ValidationError

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # 1. VALIDATION (The Modern Way)
    schema = RegisterSchema()
    try:
        # This will validate email format, password complexity, etc.
        validated_data = schema.load(data)
    except ValidationError as err:
        # Returns a nice JSON with specific errors, e.g., {"password": ["Must contain 1 number"]}
        return jsonify({"error": "Validation Failed", "messages": err.messages}), 400

    # 2. PROCEED (Use validated_data, it's clean)
    user, error = AuthService.register_user(validated_data)
    
    if error:
        return jsonify({"error": error}), 400
        
    return jsonify({"message": "User registered successfully. Please check your email to activate."}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # 1. VALIDATION
    schema = LoginSchema()
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        return jsonify({"error": "Validation Failed", "messages": err.messages}), 400

    # 2. PROCEED
    result, error = AuthService.login_user(validated_data)
    
    if error:
        return jsonify({"error": error}), 401
        
    return jsonify(result), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    # Since we use JWTs, the client just deletes the token.
    # Optionally, add logic here to blacklist the token.
    return jsonify({"message": "Logged out successfully"}), 200

@auth_bp.route('/confirm/<token>', methods=['GET'])
def confirm_email(token):
    success, message = AuthService.confirm_email(token)
    if not success:
        return jsonify({"error": message}), 400
    return jsonify({"message": message}), 200

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')
    
    # We always return 200 even if email doesn't exist (Security: prevent user enumeration)
    AuthService.request_password_reset(email) 
    return jsonify({"message": "If that email exists, a reset link has been sent."}), 200

@auth_bp.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    data = request.get_json()
    new_password = data.get('password')
    
    success, message = AuthService.reset_password(token, new_password)
    if not success:
        return jsonify({"error": message}), 400
    return jsonify({"message": message}), 200