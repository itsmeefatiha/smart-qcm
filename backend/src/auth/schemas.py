from marshmallow import Schema, fields, validate, ValidationError
import re

# --- Custom Password Validator ---
def validate_strong_password(password):
    """
    Enforces a strong password policy:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    - At least one special character (!@#$%^&*)
    """
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    if not re.search(r"[A-Z]", password):
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        raise ValidationError("Password must contain at least one lowercase letter.")
    if not re.search(r"\d", password):
        raise ValidationError("Password must contain at least one number.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValidationError("Password must contain at least one special character.")

# --- Registration Schema ---
class RegisterSchema(Schema):
    # 'fields.Email' uses the robust email-validator library automatically
    email = fields.Email(required=True, error_messages={"invalid": "Invalid email address format."})
    
    password = fields.String(required=True, validate=validate_strong_password)
    
    first_name = fields.String(required=True, validate=validate.Length(min=2, max=50))
    last_name = fields.String(required=True, validate=validate.Length(min=2, max=50))
    
    # Optional: Validate role is one of the allowed values
    role = fields.String(validate=validate.OneOf(["student", "professor", "admin", "manager"]))

# --- Login Schema ---
class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True) # No complexity check needed for login, just presence