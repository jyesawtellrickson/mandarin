from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    favourites = db.relationship('Favourite')

class Translation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(10000))
    meta = db.Column(db.String(10000)) # json
    language = db.Column(db.String(5)) # iso
    snippet_id = db.Column(db.Integer, db.ForeignKey('snippet.id'))
    stats = db.relationship('Stat')
    favourites = db.relationship('Favourite')

class Snippet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    artist = db.Column(db.String(100))
    url = db.Column(db.String(1000))
    language = db.Column(db.String(15))
    text_type = db.Column(db.String(20))
    translations = db.relationship('Translation')
    favourites = db.relationship('Favourite')

# For a translation
class Stat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_characters = db.Column(db.Integer)
    unique_characters = db.Column(db.Integer)
    score = db.Column(db.Float)
    extra_data = db.Column(db.String(1000))
    translation_id = db.Column(db.Integer, db.ForeignKey('translation.id'))

class Favourite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    snippet_id = db.Column(db.Integer, db.ForeignKey('snippet.id'))
    translation_id = db.Column(db.Integer, db.ForeignKey('translation.id'))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
