from datetime import datetime

from flask_login import UserMixin
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import db

Base = declarative_base()

location_user = db.Table('location_user', db.Model.metadata,
                         db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                         db.Column('location_id', db.Integer, db.ForeignKey('locations.id'))
                         )


class Transactions(db.Model, SerializerMixin):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship("User", back_populates="transactions", uselist=False)
    amount = db.Column(db.String(300), nullable=True, unique=False)
    type = db.Column(db.String(300), nullable=True, unique=False)


    def __init__(self, amount, type):
        self.amount = amount
        self.type = type


class Location(db.Model, SerializerMixin):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=True, unique=False)
    longitude = db.Column(db.String(300), nullable=True, unique=False)
    latitude = db.Column(db.String(300), nullable=True, unique=False)
    population = db.Column(db.Integer, nullable=True, unique=False)


    def __init__(self, title, longitude, latitude, population):
        self.title = title
        self.longitude = longitude
        self.latitude = latitude
        self.population = population

    def serialize(self):
        return {
            'title': self.title,
            'long': self.longitude,
            'lat': self.latitude,
            'population': self.population,
        }

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    about = db.Column(db.String(300), nullable=True, unique=False)
    authenticated = db.Column(db.Boolean, default=False)
    registered_on = db.Column('registered_on', db.DateTime)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    is_admin = db.Column('is_admin', db.Boolean(), nullable=False, server_default='0')
    transactions = db.relationship("Transactions", back_populates="user", cascade="all, delete")
    locations = db.relationship("Location", secondary=location_user, backref="users")
    balance = db.Column(db.Integer, unique=False)

    def __init__(self, email, password, is_admin):
        self.email = email
        self.password = password
        self.registered_on = datetime.utcnow()
        self.is_admin = is_admin

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % self.email

    def set_balance(self, new_funds):
        self.balance = new_funds

    def get_balance(self):
        return self.balance

    def add_balance(self, new_funds):
        self.balance = self.balance + new_funds
