from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)
    created = db.Column(db.DateTime, defautl=datetime.now())
    updated = db.Column(db.DateTime, defautl=datetime.now())

    def __repr__(self):
        return f'USER:  {self.username}'
    
class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=True)
    url = db.Column(db.Text, nullable=False)
    short_url = db.Column(db.String(3), nullable=False)
    visits = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, defautl=datetime.now())
    updated = db.Column(db.DateTime, defautl=datetime.now())