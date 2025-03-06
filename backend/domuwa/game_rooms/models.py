from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from domuwa.core.models import BaseDBModel

if TYPE_CHECKING:
    from domuwa.game_categories.models import GameCategory
    from domuwa.game_types.models import GameType
    from domuwa.players.models import Player
    from domuwa.questions.models import Question
    from domuwa.rankings.models import Ranking


class GameRoomQuestionsLink(SQLModel, table=True):
    __tablename__ = "game_room_questions_links"

    game_room_id: Optional[int] = Field(
        None,
        foreign_key="game_room.id",
        primary_key=True,
    )
    question_id: Optional[int] = Field(
        None,
        foreign_key="question.id",
        primary_key=True,
    )


class GameRoom(BaseDBModel):
    __tablename__ = "game_room"

    websocket: Optional[str] = Field(None, index=True)
    created_at: datetime = Field(default_factory=datetime.now)
    rounds: int
    cur_round: int

    game_type_id: Optional[int] = Field(None, foreign_key="game_type.id")
    game_type: Optional["GameType"] = Relationship(back_populates="game_rooms")

    game_category_id: Optional[int] = Field(None, foreign_key="game_category.id")
    game_category: Optional["GameCategory"] = Relationship(back_populates="game_rooms")

    questions: list["Question"] = Relationship(
        back_populates="game_rooms",
        link_model=GameRoomQuestionsLink,
    )

    players: list["Player"] = Relationship(back_populates="game_room")

    # maybe add RoundRanking
    ranking: Optional["Ranking"] = Relationship(back_populates="game_room")
