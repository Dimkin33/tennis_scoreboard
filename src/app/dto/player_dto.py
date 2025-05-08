"""PlayerDTO class that represents a Data Transfer Object (DTO) for a player."""

from dataclasses import dataclass


@dataclass
class PlayerDTO:
    """Data Transfer Object for a player."""

    id: int
    name: str

    def to_dict(self):
        """Convert the PlayerDTO instance to a dictionary."""
        return {"id": self.id, "name": self.name}

    @staticmethod
    def from_player(player):
        """Create a PlayerDTO instance from a player object."""
        return PlayerDTO(id=player.id, name=player.name)
