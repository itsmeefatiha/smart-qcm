from flask import Flask
from src.extensions import db, migrate, jwt, cors, bcrypt, mail
from src.auth import auth_bp
from src.users import users_bp
from src.documents import documents_bp

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.Config')
    app.config.from_pyfile('config.py', silent=True)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(documents_bp, url_prefix='/documents')

    return app