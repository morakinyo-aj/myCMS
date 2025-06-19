from flask_login import UserMixin
from utils import db
import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    filename = db.Column(db.String(30))
    filepath = db.Column(db.String(30))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    content_type = db.Column(db.String(20))  # 'video', 'image', 'text'
    tags = db.Column(db.String(200))  # comma-separated tags
    user = db.relationship('User', backref='contents')  # Link to User model