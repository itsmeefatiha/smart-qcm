from flask import Flask
from src.extensions import db, migrate, jwt, cors

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.Config')
    app.config.from_pyfile('config.py', silent=True)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    # Test Route
    @app.route('/')
    def hello():
        return {"message": "Database Connected Successfully!", "status": "success"}

    return app