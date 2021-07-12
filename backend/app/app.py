
from flask import Flask
from .config import Config 
from .extentions import (
    db,
    mail,
    migrate, 
    bcrypt, 
    login_manager,
)

from backend.app.blueprints.article import bp as article_bp
from backend.app.blueprints.user import bp as user_bp
from backend.app.blueprints.word import bp as word_bp
from backend.app.models import article_word_table

def create_app(settings_override = None):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    if settings_override:
        app.config.update(settings_override)

    extensions(app)

    app.register_blueprint(user_bp)
    app.register_blueprint(article_bp)
    app.register_blueprint(word_bp)

    
    return app


def extensions(app):
    """
    Register 0 or more extensions (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    return None

