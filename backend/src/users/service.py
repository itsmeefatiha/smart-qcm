from .repository import UserRepository
from .models import User, UserRole
from src.extensions import bcrypt
import os
import secrets
from PIL import Image
from flask import current_app

class UserService:
    @staticmethod
    def create_user(data, is_active=False): # <--- Added Parameter with default
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
            is_active=is_active # <--- Set the active status
        )

        return UserRepository.create_user(new_user), None
    
    @staticmethod
    def save_profile_picture(user_id, file_storage):
        """
        Saves the file, resizes it to save space, and returns the filename.
        """
        try:
            # 1. Generate a random name to prevent collisions
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(file_storage.filename)
            picture_fn = random_hex + f_ext
            
            # 2. Construct the full path
            # Make sure this folder exists: src/static/profile_pics
            picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
            
            # 3. Resize Image (Optimization)
            # We assume avatars don't need to be huge. 150x150 is standard.
            output_size = (150, 150)
            i = Image.open(file_storage)
            i.thumbnail(output_size)
            i.save(picture_path)
            
            # 4. Update Database
            user = UserRepository.get_by_id(user_id)
            if user:
                # Optional: Delete old image if it's not the default
                if user.profile_image != 'default.png':
                    old_path = os.path.join(current_app.root_path, 'static/profile_pics', user.profile_image)
                    if os.path.exists(old_path):
                        os.remove(old_path)

                user.profile_image = picture_fn
                # We need to commit this change. 
                # Since UserRepository.create_user handles adding, we might need a dedicated update method
                # Or just commit directly here since Service has access to db
                from src.extensions import db
                db.session.commit()
                return picture_fn, None
            
            return None, "User not found"
        except Exception as e:
            return None, str(e)