
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from sqlalchemy import ForeignKey
from enum import Enum

db = SQLAlchemy()

    
@dataclass
class Planets(db.Model):
    __tablename__ = 'planets'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id:int = db.Column(db.Integer, primary_key=True, unique=True)
    name:str = db.Column(db.String(250), nullable=False, unique=True)
    population:str = db.Column(db.String(250), nullable=False)
    climate:str = db.Column(db.String(250), nullable=False)
    diameter:str = db.Column(db.String(250), nullable=False)
    gravity:str = db.Column(db.String(250), nullable=False)
    def __repr__(self):
        return '<Planets %r>' % self.planets
    def serialize(self):
        return {
            "id": self.id,
            # do not serialize the password, its a security breach
        }

@dataclass
class Films(db.Model):
    __tablename__ = 'films'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id:int = db.Column(db.Integer, primary_key=True, unique=True)
    title:str = db.Column(db.String(250), nullable=False, unique=True)
    episode_id:str = db.Column(db.String(250), nullable=False)
    release_date:str = db.Column(db.String(250), nullable=False)
    director:str = db.Column(db.String(250), nullable=False)
    producer:str = db.Column(db.String(250), nullable=False)
    def __repr__(self):
        return '<Films %r>' % self.films
    def serialize(self):
        return {
            "id": self.id,
            # do not serialize the password, its a security breach
        }

@dataclass    
class People(db.Model):
    __tablename__ = 'people'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id:int = db.Column(db.Integer, primary_key=True, unique=True)
    name:str = db.Column(db.String(250), nullable=False, unique=True)
    species:str = db.Column(db.String(250), nullable=False)
    skin_color:str = db.Column(db.String(250), nullable=False)
    hair_color:str = db.Column(db.String(250), nullable=False)
    height:str = db.Column(db.String(250), nullable=False)
    homeworld:int = db.Column(db.Integer, ForeignKey(Planets.id), nullable=False)
    def __repr__(self):
        return '<People %r>' % self.people
    def serialize(self):
        return {
            "id": self.id,
            # do not serialize the password, its a security breach
        }

@dataclass     
class Users(db.Model):
    __tablename__ = 'users'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id:int = db.Column(db.Integer, primary_key=True, unique=True)
    first_name:str = db.Column(db.String(250), nullable=True)
    last_name:str = db.Column(db.String(250), nullable=True)
    email:str = db.Column(db.String(250), nullable=False, unique=True)
    username:str = db.Column(db.String(250), nullable=True)
    password = db.Column(db.VARCHAR(60), nullable=False)
    favorite = db.relationship("Favorites", backref = "users", lazy=True)
    def __repr__(self):
        return '<Users %r>' % self.username
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "is_active": self.is_active,
            "username": self.username
            # do not serialize the password, its a security breach
        }
    
class FavoriteTypeEnum(str, Enum):
    Planet= "Planet"
    People = "People"
    Films = "Films"

@dataclass 
class Favorites(db.Model):
    __tablename__ = 'favorites'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id:int = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    external_ID:int = db.Column(db.Integer, nullable=False)
    name:str = db.Column(db.String(250), nullable=False)
    type:FavoriteTypeEnum = db.Column(db.Enum(FavoriteTypeEnum), nullable=False, unique=False)
    def __repr__(self):
        return '<Favorites %r>' % self.favorites



    def serialize(self):
        return {
            "id": self.id,
            # do not serialize the password, its a security breach
        }