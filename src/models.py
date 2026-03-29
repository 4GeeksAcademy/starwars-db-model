from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    subscription_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relación: Un usuario tiene muchos favoritos
    favorites = db.relationship('Favorite', backref='user', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "subscription_date": self.subscription_date.isoformat() if self.subscription_date else None
        }

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    climate = db.Column(db.String(50))
    population = db.Column(db.String(50))
    terrain = db.Column(db.String(50))

    # Relación: Un planeta puede estar en los favoritos de muchos usuarios
    favorites = db.relationship('Favorite', backref='planet', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population,
            "terrain": self.terrain
        }

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    gender = db.Column(db.String(20))
    hair_color = db.Column(db.String(20))
    eye_color = db.Column(db.String(20))

    # Relación: Un personaje puede estar en los favoritos de muchos usuarios
    favorites = db.relationship('Favorite', backref='character', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color
        }

class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    
    # Claves foráneas
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "character_id": self.character_id
        }