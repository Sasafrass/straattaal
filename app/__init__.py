from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = "auth.login"  # View function that handles the login
login.login_message = "Please login to access this page."


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize the Flask extensions.
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    # Main blueprint.
    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    # Authentication blueprint.
    from app.auth import bp as auth_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")

    # API blueprint.
    from app.api import bp as api_bp

    app.register_blueprint(api_bp, url_prefix="/api")

    # Groups blueprint.
    from app.groups import bp as groups_bp

    app.register_blueprint(groups_bp, url_prefix="/groups")

    return app
