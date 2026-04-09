from flask import request, jsonify
from flasgger import swag_from
from . import auth_bp
from .service import AuthService
from .schemas import RegisterSchema, LoginSchema
from marshmallow import ValidationError

@auth_bp.route('/register', methods=['POST'])
@swag_from({
    'tags': ['Auth'],
    'summary': 'Register a new user',
    'consumes': ['application/json'],
    'parameters': [{
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'required': ['email', 'password', 'first_name', 'last_name'],
            'properties': {
                'email': {'type': 'string'},
                'password': {'type': 'string'},
                'first_name': {'type': 'string'},
                'last_name': {'type': 'string'},
                'role': {'type': 'string'},
                'branch_id': {'type': 'integer'},
            },
        },
    }],
    'responses': {
        201: {'description': 'User created successfully'},
        400: {'description': 'Validation error or email failure'},
    },
})
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
@swag_from({
    'tags': ['Auth'],
    'summary': 'Login a user',
    'consumes': ['application/json'],
    'parameters': [{
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'required': ['email', 'password'],
            'properties': {
                'email': {'type': 'string'},
                'password': {'type': 'string'},
            },
        },
    }],
    'responses': {
        200: {'description': 'Login successful'},
        401: {'description': 'Invalid credentials or inactive account'},
    },
})
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
@swag_from({
    'tags': ['Auth'],
    'summary': 'Logout the current user',
    'responses': {
        200: {'description': 'Logged out successfully'},
    },
})
def logout():
    # Since we use JWTs, the client just deletes the token.
    # Optionally, add logic here to blacklist the token.
    return jsonify({"message": "Logged out successfully"}), 200

@auth_bp.route('/confirm/<token>', methods=['GET'])
@swag_from({
    'tags': ['Auth'],
    'summary': 'Confirm a user email address',
    'parameters': [{
        'in': 'path',
        'name': 'token',
        'type': 'string',
        'required': True,
    }],
    'responses': {
        200: {'description': 'Account activated successfully'},
        400: {'description': 'Invalid or expired token'},
    },
})
def confirm_email(token):
    success, message = AuthService.confirm_email(token)
    if not success:
        return jsonify({"error": message}), 400
    return jsonify({"message": message}), 200

@auth_bp.route('/forgot-password', methods=['POST'])
@swag_from({
    'tags': ['Auth'],
    'summary': 'Request a password reset email',
    'consumes': ['application/json'],
    'parameters': [{
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'required': ['email'],
            'properties': {
                'email': {'type': 'string'},
            },
        },
    }],
    'responses': {
        200: {'description': 'Reset email handled'},
    },
})
def forgot_password():
    data = request.get_json()
    email = data.get('email')
    
    # We always return 200 even if email doesn't exist (Security: prevent user enumeration)
    AuthService.request_password_reset(email) 
    return jsonify({"message": "If that email exists, a reset link has been sent."}), 200

@auth_bp.route('/reset-password/<token>', methods=['POST'])
@swag_from({
    'tags': ['Auth'],
    'summary': 'Reset a password using a valid token',
    'parameters': [{
        'in': 'path',
        'name': 'token',
        'type': 'string',
        'required': True,
    }, {
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'required': ['password'],
            'properties': {
                'password': {'type': 'string'},
            },
        },
    }],
    'responses': {
        200: {'description': 'Password updated successfully'},
        400: {'description': 'Invalid or expired token'},
    },
})
def reset_password(token):
    data = request.get_json()
    new_password = data.get('password')
    
    success, message = AuthService.reset_password(token, new_password)
    if not success:
        return jsonify({"error": message}), 400
    return jsonify({"message": message}), 200