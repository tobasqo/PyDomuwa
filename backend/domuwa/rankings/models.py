from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from domuwa.game_rooms.models import GameRoom
    from domuwa.players.models import Player


class PlayerScore(SQLModel, table=True):
    __tablename__ = "player_score"

    id: int | None = Field(None, primary_key=True)
    points: float = 0.0

    player_id: Optional[int] = Field(None, foreign_key="player.id")
    player: Optional["Player"] = Relationship(
        back_populates="player_scores", sa_relationship_kwargs={"lazy": "selectin"}
    )

    ranking_id: Optional[int] = Field(None, foreign_key="ranking.id")
    ranking: Optional["Ranking"] = Relationship(back_populates="player_scores")


class Ranking(SQLModel, table=True):
    __tablename__ = "ranking"

    id: int | None = Field(None, primary_key=True)

    game_room_id: Optional[int] = Field(None, foreign_key="game_room.id")
    game_room: Optional["GameRoom"] = Relationship(back_populates="ranking")

    player_scores: list[PlayerScore] = Relationship(back_populates="ranking")
