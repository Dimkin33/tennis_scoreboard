"""Сервис для работы с игроками."""

import logging

from dto import PlayerDTO
from models import Player
from sqlalchemy.orm import Session


class PlayerService:
    """Сервис для работы с игроками."""

    def __init__(self, db: Session):
        """Инициализация сервиса сессией базы данных."""
        self.db = db

    def create_player(self, name: str) -> PlayerDTO:
        """Создать игрока, если он не существует."""
        player = self.db.query(Player).filter(Player.name == name).first()
        if not player:
            player = Player(name=name)
            self.db.add(player)
            self.db.commit()
            self.db.refresh(player)
            logging.info(f"Создан игрок: {player}")
        else:
            logging.info(f"Игрок уже существует: {player}")
        return PlayerDTO(id=player.id, name=player.name)

    def get_player_by_id(self, player_id: int) -> PlayerDTO | None:
        """Получить игрока по ID."""
        player = self.db.query(Player).filter(Player.id == player_id).first()
        if player:
            logging.info(f"Получен игрок по id={player_id}: {player}")
            return PlayerDTO(id=player.id, name=player.name)
        logging.warning(f"Игрок с id={player_id} не найден")
        return None

    def get_all_players(self) -> list[PlayerDTO]:
        """Получить всех игроков."""
        players = self.db.query(Player).all()
        logging.info(f"Получено {len(players)} игроков")
        return [PlayerDTO(id=p.id, name=p.name) for p in players]
