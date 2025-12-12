from flask_sqlalchemy import SQLAlchemy

# Global SQLAlchemy instance
# Import this in models: from src.database import db
db = SQLAlchemy()


def init_db(app):
    """
    Initialize the database with the Flask app.
    This is called inside create_app() in __init__.py.
    """

    db.init_app(app)

    # Create tables automatically only in dev mode if needed
    # In production, use flask db migrate + upgrade
    with app.app_context():
        try:
            db.create_all()
        except Exception:
            # Tables may already exist or migrations are used
            pass
