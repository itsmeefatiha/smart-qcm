from flask import Blueprint

# Create the Blueprint named 'auth'
auth_bp = Blueprint('auth', __name__)

# Import the routes so they get registered with the Blueprint
# Note: We import this at the bottom to avoid "Circular Import" errors
from . import routes