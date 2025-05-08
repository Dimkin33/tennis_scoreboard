"""Модель матча."""
from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Match(Base):
    """Модель матча."""

    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True, nullable=False)
    player1_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    player2_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    winner_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    score = Column(String, nullable=False)  # JSON string

    player1 = relationship("Player", foreign_keys=[player1_id])
    player2 = relationship("Player", foreign_keys=[player2_id])
    winner = relationship("Player", foreign_keys=[winner_id])

    def __repr__(self):
        """Строковое представление матча."""
        return (f"Match(id={self.id}, uuid='{self.uuid}', "
                f"player1={self.player1.name}, player2={self.player2.name}, "
                f"winner={self.winner.name}, score='{self.score}')")
