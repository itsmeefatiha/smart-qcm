from flask import current_app
import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

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
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = os.environ.get('BREVO_API_KEY') or current_app.config.get('BREVO_API_KEY')

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    sender_email = os.environ.get('MAIL_DEFAULT_SENDER') or current_app.config.get('MAIL_DEFAULT_SENDER')
    sender = {"name": "Smart QCM", "email": sender_email}
    to_contact = [{"email": to}]

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to_contact,
        html_content=html_content,
        sender=sender,
        subject=subject
    )

    try:
        api_instance.send_transac_email(send_smtp_email)
    except ApiException as e:
        current_app.logger.error(f"Brevo API Error: {e}")
        raise