# This file has the SQLAlchemy models in OOP form to represent the datastructure. The application will have three main tables

# User - This will store user information and authentication details
# Ticket - This will represent the helpdesk tickets
# Comment - This will store the comments on the tickets

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    # The relationships
    tickets_created = db.relationship('Ticket', backref='author', lazy='dynamic', foreign_keys='Ticket.author_id')
    tickets_assigned = db.relationship('Ticket', backref='assigned_user', lazy='dynamic', foreign_keys='Ticket.assigned_to')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    # To set and hash the user password when it goes into the database
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Check password against hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='open')
    priority = db.Column(db.String(20), default='medium')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # Foreign keys
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'))

    comments = db.relationship('Comment', backref='ticket', lazy='dynamic', cascade='all, delete-orphan')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)