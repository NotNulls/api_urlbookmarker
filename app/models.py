from datetime import datetime
import string
import random
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager


db = SQLAlchemy()
login = LoginManager()
login.login_view= 'auth.login'
login.login_message = ('Please login to access this page.')

class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)
    created = db.Column(db.DateTime, default=datetime.now())
    updated = db.Column(db.DateTime, default=datetime.now())
    bookmarks = db.relationship('Bookmark', backref="user")
    
    def __repr__(self):
        return f'USER:  {self.username}'
    
    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
class Bookmark(db.Model, UserMixin):

    __tablename__ = "bookmark"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False)
    short_url = db.Column(db.String(3), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    visits = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.now())
    updated = db.Column(db.DateTime, default=datetime.now())

    def generate_short_characters(self):
        characters = string.digits+string.ascii_letters
        pick_chars = ''.join(random.choices(characters,k=3))

        link = self.query.filter_by(short_url=pick_chars).first()

        if link:
            self.generate_short_characters()
        else:
            return pick_chars
 
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.short_url = self.generate_short_characters()

    def __repr__(self):
        return f'BOOKMARK:  {self.url}'