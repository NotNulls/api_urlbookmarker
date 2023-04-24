from flask import Flask
from config import Config
from app.auth.auth import auth
from app.bookmarks.bookmarks import bookmarks
from flask_sqlalchemy import SQLAlchemy
from app import models



def create_app(config_class=Config, test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    from app.models import db
    db.init_app(app)


    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)

    return app


from app import models
