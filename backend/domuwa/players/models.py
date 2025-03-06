from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship

from domuwa.core.models import BaseDBModel

if TYPE_CHECKING:
    from domuwa.answers.models import Answer
    from domuwa.game_rooms.models import GameRoom
    from domuwa.questions.models import Question
    from domuwa.rankings.models import PlayerScore
    from domuwa.users.models import User


class Player(BaseDBModel):
    __tablename__ = "player"

    id: int = Field(primary_key=True, foreign_key="user.id")
    user: "User" = Relationship(back_populates="player")

    games_played: int = 0
    games_won: int = 0

    questions: list["Question"] = Relationship(back_populates="author")
    answers: list["Answer"] = Relationship(back_populates="author")

    game_room_id: Optional[int] = Field(None, foreign_key="game_room.id", nullable=True)
    game_room: Optional["GameRoom"] = Relationship(back_populates="players")

    player_scores: list["PlayerScore"] = Relationship(back_populates="player")
