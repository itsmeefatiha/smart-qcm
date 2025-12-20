from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from src.users.models import User

def role_required(allowed_roles):
    """
    Decorator to restrict access to specific user roles.
    
    Usage:
        from src.auth.models import UserRole
        @role_required([UserRole.MANAGER, UserRole.ADMIN])
    
    Args:
        allowed_roles (list): A list of UserRole enum values that are permitted.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            # 1. Ensure a valid JWT is present in the request
            verify_jwt_in_request()
            
            # 2. Get the User ID from the token
            user_id = get_jwt_identity()
            
            # 3. Fetch the user from the database
            user = User.query.get(user_id)
            
            if not user:
                return jsonify({"error": "User not found"}), 404

            # 4. Check if the user's role is in the list of allowed roles
            # user.role is an Enum, so we compare it directly to the allowed Enum list
            if user.role not in allowed_roles:
                return jsonify({
                    "error": "Unauthorized access: Insufficient permissions"
                }), 403

            # 5. Proceed to the actual route function
            return fn(*args, **kwargs)
            
        return decorator
    return wrapper