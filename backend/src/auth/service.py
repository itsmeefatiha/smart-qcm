from src.extensions import bcrypt
from flask_jwt_extended import create_access_token
from .repository import AuthRepository
from src.users.service import UserService

class AuthService:
    @staticmethod
    def register_user(data):
        # We delegate creation to UserService to keep logic centralized
        return UserService.create_user(data)

    @staticmethod
    def login_user(data):
        email = data.get('email')
        password = data.get('password')

        user = AuthRepository.find_user_by_email(email)

        if user and bcrypt.check_password_hash(user.password_hash, password):
            # Create JWT Token
            # identity=user.id means get_jwt_identity() will return the ID
            access_token = create_access_token(identity=user.id)
            return {
                "access_token": access_token,
                "user": user.to_dict()
            }, None
        
        return None, "Invalid email or password"