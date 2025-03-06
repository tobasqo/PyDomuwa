from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from domuwa.core.models import BaseDBModel
from domuwa.game_types.constants import GameTypeChoices

if TYPE_CHECKING:
    from domuwa.answers.models import Answer
    from domuwa.game_rooms.models import GameRoom
    from domuwa.questions.models import Question


class GameType(BaseDBModel):
    __tablename__ = "game_type"

    name: GameTypeChoices = Field(index=True, unique=True)

    questions: list["Question"] = Relationship(back_populates="game_type")
    answers: list["Answer"] = Relationship(back_populates="game_type")
    game_rooms: list["GameRoom"] = Relationship(back_populates="game_type")
