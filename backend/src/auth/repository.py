# The Auth package mainly uses the User repository, 
# but we can add token-specific DB logic here if needed (like blacklisting).
# For now, we reuse the User repository to keep it DRY.
from src.users.repository import UserRepository

class AuthRepository:
    @staticmethod
    def find_user_by_email(email):
        return UserRepository.get_by_email(email)