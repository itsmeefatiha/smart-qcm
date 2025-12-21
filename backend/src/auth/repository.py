from src.users.repository import UserRepository

class AuthRepository:
    @staticmethod
    def find_user_by_email(email):
        return UserRepository.get_by_email(email)