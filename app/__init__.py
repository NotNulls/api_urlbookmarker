from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from app.models import login

migrate = Migrate()


def create_app(config_class=Config, test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    from app.models import db
    from app.auth.auth import auth as auth_bp
    from app.bookmarks.bookmarks import bookmarks as bookmarks_bp
    from app.errors import bp as errors_bp
    from app.errors import handlers



    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login.init_app(app)

    JWTManager(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(bookmarks_bp)
    app.register_blueprint(errors_bp, handlers=handlers)

    return app
