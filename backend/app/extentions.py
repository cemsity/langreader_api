from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail 
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
bcrypt = Bcrypt()
migrate = Migrate()
