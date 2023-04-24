import os

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'use secrets to generate key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', '') or ('sqlite:///' + os.path.join(base_dir, 'bookmarks.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False