from src.extensions import bcrypt, db
from flask_jwt_extended import create_access_token
from .repository import AuthRepository
from src.users.service import UserService
from .security import generate_token, verify_token, send_email

class AuthService:
    @staticmethod
    def register_user(data):
        user, error = UserService.create_user(data, is_active=False)
        if error:
            return None, error

        token = generate_token(user.email, salt='email-confirm')

        activation_link = f"http://localhost:5173/activate/{token}"
        
        html = f"""
        <p>Welcome {user.first_name}!</p>
        <p>Please click here to activate your account:</p>
        <a href="{activation_link}">Activate Account</a>
        """
        try:
            send_email(user.email, "Activate your Smart QCM Account", html)
        except Exception as e:
            return None, "User created but email failed to send."

        return user, None

    @staticmethod
    def confirm_email(token):
        email = verify_token(token, salt='email-confirm')
        if not email:
            return False, "Invalid or expired token"
        
        user = AuthRepository.find_user_by_email(email)
        if not user:
            return False, "User not found"
        
        user.is_active = True
        db.session.commit()
        return True, "Account activated successfully"

    @staticmethod
    def login_user(data):
        email = data.get('email')
        password = data.get('password')
        user = AuthRepository.find_user_by_email(email)

        if user and bcrypt.check_password_hash(user.password_hash, password):
            if not user.is_active:
                return None, "Please activate your account first (check your email)."

            access_token = create_access_token(identity=str(user.id))
            return {
                "access_token": access_token,
                "user": user.to_dict()
            }, None
        
        return None, "Invalid email or password"

    @staticmethod
    def request_password_reset(email):
        user = AuthRepository.find_user_by_email(email)
        if not user:
            return None, "User not found"

        token = generate_token(user.email, salt='password-reset')
        reset_link = f"http://localhost:5173/reset-password/{token}"
        
        html = f"<p>Click here to reset your password:</p><a href='{reset_link}'>Reset Password</a>"
        send_email(user.email, "Password Reset Request", html)
        return True, "Reset email sent"

    @staticmethod
    def reset_password(token, new_password):
        email = verify_token(token, salt='password-reset')
        if not email:
            return False, "Invalid or expired token"

        user = AuthRepository.find_user_by_email(email)
        if not user:
            return False, "User not found"

        user.password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
        db.session.commit()
        return True, "Password updated successfully"