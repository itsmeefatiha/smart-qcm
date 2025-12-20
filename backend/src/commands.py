import click
from flask.cli import with_appcontext
from src.extensions import db, bcrypt
from src.users.models import User, UserRole

@click.command(name='create_admin')
@click.argument('email')
@click.argument('password')
@with_appcontext
def create_admin(email, password):
    """Creates a superuser admin with the given email and password."""
    
    # 1. Check if email exists
    if User.query.filter_by(email=email).first():
        print(f"Error: User with email {email} already exists.")
        return

    # 2. Hash Password
    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')

    # 3. Create Admin User
    admin = User(
        email=email,
        password_hash=hashed_pw,
        first_name="Super",
        last_name="Admin",
        role=UserRole.ADMIN,
        is_active=True,   # Active immediately
        branch_id=None    # Admins don't belong to a branch
    )

    # 4. Save
    db.session.add(admin)
    db.session.commit()
    
    print(f"Success! Admin {email} created.")