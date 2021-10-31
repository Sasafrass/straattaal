"""Main initialization for the flask application."""
from flask import Flask
from flask_session import Session
from config import Config
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
sess = Session()
login.login_view = "auth.login"  # View function that handles the login
login.login_message = "Please login to access this page."


def create_app(config_class=Config):
    """Create the flask application.
    
    Args:
        config_class: Config class to be used to initialize the Flask application with.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    # TODO: Maybe refactor setting SESSION_TYPE to Config class.
    # TODO: Change SESSION_TYPE to 'redis' when we have our Redis instance up and running.
    # app.config['SESSION_TYPE'] = 'redis'
    app.config["SESSION_TYPE"] = "filesystem"

    # Initialize the Flask extensions.
    db.init_app(app)
    with app.app_context():
        if db.engine.url.drivername == 'sqlite':
            migrate.init_app(app, db, render_as_batch=True)
        else:
            migrate.init_app(app, db)
    bootstrap.init_app(app)
    login.init_app(app)
    sess.init_app(app)

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

    # Users blueprint.
    from app.users import bp as users_bp

    app.register_blueprint(users_bp, url_prefix="/users")

    return app
