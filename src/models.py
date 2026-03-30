from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, DateTime
from datetime import datetime, timezone
from typing import List, Optional

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(80), nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    subscription_date: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relación: Un usuario tiene muchos favoritos (1 a N)
    favorites: Mapped[List["Favorite"]] = relationship(back_populates="user")

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
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    # Usamos Optional porque estos campos podrían estar vacíos (nullable=True por defecto)
    climate: Mapped[Optional[str]] = mapped_column(String(50))
    population: Mapped[Optional[str]] = mapped_column(String(50))
    terrain: Mapped[Optional[str]] = mapped_column(String(50))

    # Relación: Un planeta puede estar en los favoritos de muchos usuarios
    favorites: Mapped[List["Favorite"]] = relationship(back_populates="planet")

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
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    gender: Mapped[Optional[str]] = mapped_column(String(20))
    hair_color: Mapped[Optional[str]] = mapped_column(String(20))
    eye_color: Mapped[Optional[str]] = mapped_column(String(20))

    # Relación: Un personaje puede estar en los favoritos de muchos usuarios
    favorites: Mapped[List["Favorite"]] = relationship(back_populates="character")

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
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    planet_id: Mapped[Optional[int]] = mapped_column(ForeignKey('planet.id'))
    character_id: Mapped[Optional[int]] = mapped_column(ForeignKey('character.id'))

    user: Mapped["User"] = relationship(back_populates="favorites")
    planet: Mapped[Optional["Planet"]] = relationship(back_populates="favorites")
    character: Mapped[Optional["Character"]] = relationship(back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "character_id": self.character_id
        }