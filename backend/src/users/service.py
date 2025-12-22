from .repository import UserRepository
from .models import User, UserRole
from src.extensions import bcrypt, db
import os
import secrets
from PIL import Image
from flask import current_app

class UserService:
    @staticmethod
    def create_user(data, is_active=False):
        # 1. Check uniqueness
        if UserRepository.get_by_email(data.get('email')):
            return None, "Email already registered"

        # 2. Hash Password
        hashed_pw = bcrypt.generate_password_hash(data.get('password')).decode('utf-8')

        # 3. Handle Branch Logic
        role = UserRole(data.get('role', 'student'))
        branch_id = data.get('branch_id')

        # VALIDATION: If role is Student, Branch is MANDATORY
        if role == UserRole.STUDENT and not branch_id:
             return None, "Students must be assigned to a Branch."

        # 4. Create User
        new_user = User(
            email=data.get('email'),
            password_hash=hashed_pw,
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            role=role,
            branch_id=branch_id,
            is_active=is_active
        )

        return UserRepository.create_user(new_user), None
    
    @staticmethod
    def save_profile_picture(user_id, file_storage):
        try:
            # 1. Generate random filename
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(file_storage.filename)
            picture_fn = random_hex + f_ext
            
            # 2. Build Path Correctly (Safe for Windows/Mac)
            # This points to: backend/src/static/profile_pics/
            folder_path = os.path.join(current_app.root_path, 'static', 'profile_pics')
            
            # --- CRITICAL FIX: Create directory if it doesn't exist ---
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            # ----------------------------------------------------------

            picture_path = os.path.join(folder_path, picture_fn)
            
            # 3. Resize and Save
            output_size = (150, 150)
            i = Image.open(file_storage)
            i.thumbnail(output_size)
            i.save(picture_path)
            
            # 4. Update Database
            user = UserRepository.get_by_id(user_id)
            if user:
                # Delete old image if it exists and isn't default
                if user.profile_image and 'default' not in user.profile_image:
                    old_path = os.path.join(folder_path, user.profile_image)
                    if os.path.exists(old_path):
                        try:
                            os.remove(old_path)
                        except:
                            pass # Don't crash if delete fails

                user.profile_image = picture_fn
                db.session.commit()
                return picture_fn, None
            
            return None, "User not found"
        except Exception as e:
            return None, str(e)