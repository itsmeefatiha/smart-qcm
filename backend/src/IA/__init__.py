from flask import Blueprint

ia_bp = Blueprint('ia', __name__)

from . import routes