from flask import request, jsonify
from . import auth_bp
from .service import AuthService
from .schemas import REGISTER_SCHEMA, LOGIN_SCHEMA

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Simple Validation
    if not all(k in data for k in REGISTER_SCHEMA):
        return jsonify({"error": "Missing fields"}), 400

    user, error = AuthService.register_user(data)
    
    if error:
        return jsonify({"error": error}), 400
        
    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not all(k in data for k in LOGIN_SCHEMA):
        return jsonify({"error": "Missing email or password"}), 400

    result, error = AuthService.login_user(data)
    
    if error:
        return jsonify({"error": error}), 401
        
    return jsonify(result), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    # Since we use JWTs, the client just deletes the token.
    # Optionally, add logic here to blacklist the token.
    return jsonify({"message": "Logged out successfully"}), 200