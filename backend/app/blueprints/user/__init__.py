from flask import Blueprint

bp = Blueprint('user', __name__)

from backend.app.blueprints.user import routes, model