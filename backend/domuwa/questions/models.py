from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship

from domuwa.core.models import BaseDBModel
from domuwa.game_rooms.models import GameRoomQuestionsLink
from domuwa.questions.constants import TEXT_MAX_LEN, TEXT_MIN_LEN

if TYPE_CHECKING:
    from domuwa.answers.models import Answer
    from domuwa.game_rooms.models import GameRoom
    from domuwa.game_types.models import GameType
    from domuwa.players.models import Player
    from domuwa.qna_categories.models import QnACategory


class Question(BaseDBModel):
    __tablename__ = "question"

    text: str = Field(min_length=TEXT_MIN_LEN, max_length=TEXT_MAX_LEN)
    excluded: bool = Field(False, index=True)
    deleted: bool = Field(False, index=True)

    author_id: Optional[int] = Field(None, foreign_key="player.id")
    author: Optional["Player"] = Relationship(back_populates="questions")

    game_type_id: Optional[int] = Field(None, foreign_key="game_type.id")
    game_type: Optional["GameType"] = Relationship(back_populates="questions")

    game_category_id: Optional[int] = Field(None, foreign_key="qna_category.id")
    game_category: Optional["QnACategory"] = Relationship(back_populates="questions")

    prev_version_id: Optional[int] = Field(None, foreign_key="question.id")
    prev_version: Optional["Question"] = Relationship(
        back_populates="next_versions",
        sa_relationship_kwargs={"remote_side": "Question.id"},
    )
    next_versions: list["Question"] = Relationship(back_populates="prev_version")

    answers: list["Answer"] = Relationship(back_populates="question")

    game_rooms: list["GameRoom"] = Relationship(
        back_populates="questions",
        link_model=GameRoomQuestionsLink,
    )
