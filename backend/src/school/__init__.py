from flask import Blueprint

school_bp = Blueprint('school', __name__)
from . import routes