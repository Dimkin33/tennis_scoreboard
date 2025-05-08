"""Модель игрока, которая хранит информацию о каждом игроке в базе данных."""

from sqlalchemy import Column, Integer, String

from .database import Base


class Player(Base):
    """Модель игрока."""

    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    def __repr__(self):
        """Строковое представление игрока."""
        return f"Player(id={self.id}, name='{self.name}')"
