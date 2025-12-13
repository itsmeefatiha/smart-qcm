from .repository import UserRepository
from .models import User, UserRole
from src.extensions import bcrypt

class UserService:
    @staticmethod
    def create_user(data):
        # Check if user already exists
        if UserRepository.get_by_email(data.get('email')):
            return None, "Email already registered"

        # Hash password
        hashed_pw = bcrypt.generate_password_hash(data.get('password')).decode('utf-8')

        # Create user instance
        new_user = User(
            email=data.get('email'),
            password_hash=hashed_pw,
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            role=UserRole(data.get('role', 'student'))  # Default to student
        )

        return UserRepository.create_user(new_user), None