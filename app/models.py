

from app import db
from flask_login import UserMixin


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True )
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    def __repr__(self):
        return '<User {}>'.format(self.username)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True,index=True)
    head = db.Column(db.String(255),index=True)
    body = db.Column(db.Text)
    tag = db.Column(db.String)
    timestamp = db.Column(db.DateTime,index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    img_url = db.Column(db.String,default="https://i.imgur.com/DiQqxRx.png")
    
class Tag(db.Model):
    id = db.Column(db.Integer,primary_key=True,index=True)
    name = db.Column(db.String(50))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))


