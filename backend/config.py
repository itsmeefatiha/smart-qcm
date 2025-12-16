import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:password@localhost:5432/smartquiz"
    SQLALCHEMY_TRACK_MODIFICATIONS = False