from flask import Flask
from config import Config
from app.auth import auth
from app.bookmarks import bookmarks




def create_app(config_class=Config, test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)

    return app  