from flask import current_app
import resend
import os

def generate_token(email, salt):
    from itsdangerous import URLSafeTimedSerializer
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=salt)

def verify_token(token, salt, expiration=3600):
    from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=salt, max_age=expiration)
        return email
    except (SignatureExpired, BadSignature):
        return None

def send_email(to, subject, html_content):
    resend.api_key = os.environ.get("RESEND_API_KEY")
    
    params = {
        "from": os.environ.get("RESEND_FROM_EMAIL", "onboarding@resend.dev"),
        "to": [to],
        "subject": subject,
        "html": html_content,
    }
    
    resend.Emails.send(params)