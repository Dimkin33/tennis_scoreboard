"""Сервис для работы с матчами."""
import json
import uuid

from sqlalchemy.orm import Session

from app.dto import MatchDTO, PlayerDTO
from app.models import Match, Player


class MatchService:
    """Сервис для работы с матчами."""

    def __init__(self, db: Session):
        """Инициализация сервиса сессией базы данных."""
        self.db = db

    def create_match(self, player1_id: int, player2_id: int) -> MatchDTO:
        """Создать новый матч."""
        player1 = self.db.query(Player).filter(Player.id == player1_id).first()
        player2 = self.db.query(Player).filter(Player.id == player2_id).first()
        if not (player1 and player2):
            raise ValueError("Один из игроков не найден")

        match_uuid = str(uuid.uuid4())
        match = Match(
            uuid=match_uuid,
            player1_id=player1_id,
            player2_id=player2_id,
            winner_id=None,
            score=json.dumps({"player1": 0, "player2": 0})
        )
        self.db.add(match)
        self.db.commit()
        self.db.refresh(match)

        return MatchDTO(
            id=match.id,
            uuid=match.uuid,
            player1=PlayerDTO(id=player1.id, name=player1.name),
            player2=PlayerDTO(id=player2.id, name=player2.name),
            winner=None,
            score=match.score
        )

    def update_score(self, match_uuid: str, player_id: int, points: int) -> MatchDTO:
        """Обновить счёт матча."""
        match = self.db.query(Match).filter(Match.uuid == match_uuid).first()
        if not match:
            raise ValueError("Матч не найден")

        score = json.loads(match.score)
        if match.player1_id == player_id:
            score["player1"] += points
        elif match.player2_id == player_id:
            score["player2"] += points
        else:
            raise ValueError("Игрок не участвует в матче")

        match.score = json.dumps(score)
        self.db.commit()
        self.db.refresh(match)

        player1 = self.db.query(Player).filter(Player.id == match.player1_id).first()
        player2 = self.db.query(Player).filter(Player.id == match.player2_id).first()
        winner = self.db.query(Player).filter(Player.id == match.winner_id).first() if match.winner_id else None

        return MatchDTO(
            id=match.id,
            uuid=match.uuid,
            player1=PlayerDTO(id=player1.id, name=player1.name),
            player2=PlayerDTO(id=player2.id, name=player2.name),
            winner=PlayerDTO(id=winner.id, name=winner.name) if winner else None,
            score=match.score
        )

    def set_winner(self, match_uuid: str, winner_id: int) -> MatchDTO:
        """Установить победителя матча."""
        match = self.db.query(Match).filter(Match.uuid == match_uuid).first()
        if not match:
            raise ValueError("Матч не найден")

        if winner_id not in [match.player1_id, match.player2_id]:
            raise ValueError("Победитель не участвует в матче")

        match.winner_id = winner_id
        self.db.commit()
        self.db.refresh(match)

        player1 = self.db.query(Player).filter(Player.id == match.player1_id).first()
        player2 = self.db.query(Player).filter(Player.id == match.player2_id).first()
        winner = self.db.query(Player).filter(Player.id == match.winner_id).first()

        return MatchDTO(
            id=match.id,
            uuid=match.uuid,
            player1=PlayerDTO(id=player1.id, name=player1.name),
            player2=PlayerDTO(id=player2.id, name=player2.name),
            winner=PlayerDTO(id=winner.id, name=winner.name) if winner else None,
            score=match.score
        )

    def get_match_by_uuid(self, match_uuid: str) -> MatchDTO | None:
        """Получить матч по UUID."""
        match = self.db.query(Match).filter(Match.uuid == match_uuid).first()
        if not match:
            return None

        player1 = self.db.query(Player).filter(Player.id == match.player1_id).first()
        player2 = self.db.query(Player).filter(Player.id == match.player2_id).first()
        winner = self.db.query(Player).filter(Player.id == match.winner_id).first() if match.winner_id else None

        return MatchDTO(
            id=match.id,
            uuid=match.uuid,
            player1=PlayerDTO(id=player1.id, name=player1.name),
            player2=PlayerDTO(id=player2.id, name=player2.name),
            winner=PlayerDTO(id=winner.id, name=winner.name) if winner else None,
            score=match.score
        )

    def get_all_matches(self) -> list[MatchDTO]:
        """Получить все матчи."""
        matches = self.db.query(Match).all()
        result = []
        for match in matches:
            player1 = self.db.query(Player).filter(Player.id == match.player1_id).first()
            player2 = self.db.query(Player).filter(Player.id == match.player2_id).first()
            winner = self.db.query(Player).filter(Player.id == match.winner_id).first() if match.winner_id else None

            result.append(MatchDTO(
                id=match.id,
                uuid=match.uuid,
                player1=PlayerDTO(id=player1.id, name=player1.name),
                player2=PlayerDTO(id=player2.id, name=player2.name),
                winner=PlayerDTO(id=winner.id, name=winner.name) if winner else None,
                score=match.score
            ))
        return result