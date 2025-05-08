"""DTO (Data Transfer Object) для матча."""

import json
from dataclasses import dataclass

from dto.player_dto import PlayerDTO


@dataclass
class MatchDTO:
    """DTO (Data Transfer Object) для матча."""

    id: int
    uuid: str
    player1: PlayerDTO
    player2: PlayerDTO
    winner: PlayerDTO
    score: dict  # Десериализованный JSON

    def to_dict(self):
        """Преобразование MatchDTO в словарь."""
        return {
            "id": self.id,
            "uuid": self.uuid,
            "player1": self.player1.to_dict(),
            "player2": self.player2.to_dict(),
            "winner": self.winner.to_dict(),
            "score": self.score,
        }

    @staticmethod
    def from_match(match):
        """Создание MatchDTO из объекта матча."""
        return MatchDTO(
            id=match.id,
            uuid=match.uuid,
            player1=PlayerDTO.from_player(match.player1),
            player2=PlayerDTO.from_player(match.player2),
            winner=PlayerDTO.from_player(match.winner),
            score=json.loads(match.score),
        )
