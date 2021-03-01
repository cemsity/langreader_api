from flask import Blueprint

bp = Blueprint('word', __name__)

from backend.app.blueprints.word import routes, model