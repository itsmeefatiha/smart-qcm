import enum
from datetime import datetime
from src.extensions import db

class UserRole(enum.Enum):
    ADMIN = "admin"
    PROFESSOR = "professor"
    STUDENT = "student"
    MANAGER = "manager"

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.STUDENT, nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=True)
    profile_image = db.Column(db.String(120), nullable=False, default='default.png')
    # Relationship to access branch name easily (user.branch.name)
    branch = db.relationship('Branch', backref='users', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "role": self.role.value,
            "branch": self.branch.name if self.branch else None,
            "profile_image_url": f"http://localhost:5000/static/profile_pics/{self.profile_image}",
            "created_at": self.created_at.isoformat()
        }