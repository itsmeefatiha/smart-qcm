from flask import Blueprint

qcm_bp = Blueprint('qcm', __name__)

from . import routes