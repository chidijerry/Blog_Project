from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from datetime import datetime
from flask_login import UserMixin


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)  # Removed unique=True
    is_active = db.Column(db.Boolean, default=True)


    # hashes passwords
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # checks password that has been hashed
    def check_password(self, password):
        return check_password_hash(self.password, password)

    # Define the relationship
    posts = db.relationship('BlogPost', backref='admin', lazy='dynamic')

    def get_id(self):
        return self.id


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
