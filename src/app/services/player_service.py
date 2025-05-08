"""Сервис для работы с игроками."""

from sqlalchemy.orm import Session

from app.dto import PlayerDTO
from app.models import Player


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
        return PlayerDTO(id=player.id, name=player.name)

    def get_player_by_id(self, player_id: int) -> PlayerDTO | None:
        """Получить игрока по ID."""
        player = self.db.query(Player).filter(Player.id == player_id).first()
        if player:
            return PlayerDTO(id=player.id, name=player.name)
        return None

    def get_all_players(self) -> list[PlayerDTO]:
        """Получить всех игроков."""
        players = self.db.query(Player).all()
        return [PlayerDTO(id=p.id, name=p.name) for p in players]
