from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from domuwa.answers.constants import TEXT_MAX_LEN, TEXT_MIN_LEN

if TYPE_CHECKING:
    from domuwa.game_types.models import GameType
    from domuwa.players.models import Player
    from domuwa.qna_categories.models import QnACategory
    from domuwa.questions.models import Question


class Answer(SQLModel, table=True):
    __tablename__ = "answer"

    id: int | None = Field(None, primary_key=True)
    text: str = Field(min_length=TEXT_MIN_LEN, max_length=TEXT_MAX_LEN)
    excluded: bool = Field(False, index=True)
    deleted: bool = Field(False, index=True)

    author_id: Optional[int] = Field(None, foreign_key="player.id")
    author: Optional["Player"] = Relationship(back_populates="answers")

    game_type_id: Optional[int] = Field(None, foreign_key="game_type.id")
    game_type: Optional["GameType"] = Relationship(back_populates="answers")

    game_category_id: Optional[int] = Field(None, foreign_key="qna_category.id")
    game_category: Optional["QnACategory"] = Relationship(back_populates="answers")

    prev_version_id: Optional[int] = Field(None, foreign_key="answer.id")
    prev_version: Optional["Answer"] = Relationship(
        back_populates="next_versions",
        sa_relationship_kwargs={"remote_side": "Answer.id"},
    )
    next_versions: list["Answer"] = Relationship(back_populates="prev_version")

    question_id: Optional[int] = Field(None, foreign_key="question.id", nullable=True)
    question: Optional["Question"] = Relationship(back_populates="answers")
