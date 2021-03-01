from flask import Blueprint

bp = Blueprint('article', __name__)

from backend.app.blueprints.article import routes, model