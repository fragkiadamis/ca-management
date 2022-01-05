# third-party imports
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# from config import app_config

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "public.homepage"
    migrate = Migrate(app, db)

    from app import models

    # from .ca import ca as admin_blueprint
    from .ca import ca as ca_blueprint
    app.register_blueprint(ca_blueprint, url_prefix='/ca')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .public import home as home_blueprint
    app.register_blueprint(home_blueprint)

    return app
