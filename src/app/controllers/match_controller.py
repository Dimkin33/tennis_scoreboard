"""# Placeholder for Python module."""
# Зависит от PYTHONPATH=src/app
from dto import MatchDTO  #только для типизации
from services import MatchService, PlayerService
from sqlalchemy.orm import Session


class MatchController:
    """Контроллер для работы с матчами."""

    def __init__(self, db: Session):
        """Инициализация контроллера матчей."""
        self.player_service = PlayerService(db)
        self.match_service = MatchService(db)

    def create_match(self, player1_name: str, player2_name: str) -> MatchDTO:
        """Создать новый матч."""
        player1 = self.player_service.create_player(player1_name)
        player2 = self.player_service.create_player(player2_name)
        return self.match_service.create_match(player1.id, player2.id)

    def update_score(self, match_uuid: str, player_id: int, points: int) -> MatchDTO:
        """Обновить счёт матча."""
        return self.match_service.update_score(match_uuid, player_id, points)

    def get_all_matches(self) -> list[MatchDTO]:
        """Получить все матчи."""
        return self.match_service.get_all_matches()
