from flask import Flask
from config import Config
from src.extensions import db, migrate, jwt, cors

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    # Test Route
    @app.route('/')
    def hello():
        return {"message": "Database Connected Successfully!", "status": "success"}

    return app