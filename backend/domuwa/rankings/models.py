from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship

from domuwa.core.models import BaseDBModel

if TYPE_CHECKING:
    from domuwa.game_rooms.models import GameRoom
    from domuwa.players.models import Player


class PlayerScore(BaseDBModel):
    __tablename__ = "player_score"

    points: float = 0.0

    player_id: Optional[int] = Field(None, foreign_key="player.id")
    player: Optional["Player"] = Relationship(back_populates="player_scores")

    ranking_id: Optional[int] = Field(None, foreign_key="ranking.id")
    ranking: Optional["Ranking"] = Relationship(back_populates="player_scores")


class Ranking(BaseDBModel):
    __tablename__ = "ranking"

    game_room_id: Optional[int] = Field(None, foreign_key="game_room.id")
    game_room: Optional["GameRoom"] = Relationship(back_populates="ranking")

    player_scores: list["PlayerScore"] = Relationship(back_populates="ranking")
