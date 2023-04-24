from datetime import datetime
import string
import random
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)
    created = db.Column(db.DateTime, default=datetime.now())
    updated = db.Column(db.DateTime, default=datetime.now())
    bookmarks = db.relationship('Bookmark', backref="user")
    

    def __repr__(self):
        return f'USER:  {self.username}'
    
class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=True)
    url = db.Column(db.Text, nullable=False)
    short_url = db.Column(db.String(3), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    visits = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.now())
    updated = db.Column(db.DateTime, default=datetime.now())

    def generate_short_characters(self):
        characters = string.digints+string.ascii_letters
        pick_chars = ''.join(random.choice(characters,k=3))

        link = self.query.filter_by(short_url=pick_chars).first()

        if link:
            self.generate_short_characters()
        else:
            return pick_chars
 
    def __init__(self) -> None:
        super().__init__()

        self.short_url = self.genetate_short_characters()

    def __repr__(self):
        return f'BOOKMARK:  {self.url}'