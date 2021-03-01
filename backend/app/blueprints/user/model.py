import datetime
from backend.app.extentions import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    articles = db.relationship('Article',backref="user", lazy=True)
    words = db.relationship('Word', backref="user", lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)