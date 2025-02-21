from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from domuwa.models.game_type import GameType, GameTypeRead
    from domuwa.models.player import Player, PlayerRead
    from domuwa.models.qna_category import QnACategory, QnACategoryRead
    from domuwa.models.question import Question, QuestionRead


TEXT_MIN_LEN = 1
TEXT_MAX_LEN = 250


class AnswerBase(SQLModel):
    text: str = Field(min_length=TEXT_MIN_LEN, max_length=TEXT_MAX_LEN)
    excluded: bool = False
    author_id: int
    game_type_id: int
    game_category_id: int
    question_id: int | None = None


class Answer(SQLModel, table=True):
    __tablename__ = "answer"

    id: Optional[int] = Field(default=None, primary_key=True)
    text: str = Field(min_length=TEXT_MIN_LEN, max_length=TEXT_MAX_LEN)
    excluded: bool = Field(default=False, index=True)
    deleted: bool = Field(False, index=True)

    author_id: Optional[int] = Field(default=None, foreign_key="player.id")
    author: Optional["Player"] = Relationship(back_populates="answers")

    game_type_id: Optional[int] = Field(default=None, foreign_key="game_type.id")
    game_type: Optional["GameType"] = Relationship(back_populates="answers")

    game_category_id: Optional[int] = Field(default=None, foreign_key="qna_category.id")
    game_category: Optional["QnACategory"] = Relationship(back_populates="answers")

    prev_version_id: Optional[int] = Field(None, foreign_key="answer.id")
    prev_version: Optional["Answer"] = Relationship(
        back_populates="next_versions",
        sa_relationship_kwargs={"remote_side": "Answer.id"},
    )
    next_versions: list["Answer"] = Relationship(back_populates="prev_version")

    question_id: Optional[int] = Field(
        default=None,
        foreign_key="question.id",
        nullable=True,
    )
    question: Optional["Question"] = Relationship(back_populates="answers")


class AnswerCreate(SQLModel):
    text: str = Field(min_length=TEXT_MIN_LEN, max_length=TEXT_MAX_LEN)
    author_id: int | None = None  # updated from `get_current_user` dependency
    game_type_id: int
    game_category_id: int
    question_id: int | None = None


class AnswerUpdate(SQLModel):
    text: str | None = Field(None, min_length=TEXT_MIN_LEN, max_length=TEXT_MAX_LEN)
    excluded: bool | None = None
    author_id: int | None = None
    game_type_id: int | None = None
    game_category_id: int | None = None
    question_id: int | None = None


class AnswerRead(SQLModel):
    id: int
    text: str = Field(min_length=TEXT_MIN_LEN, max_length=TEXT_MAX_LEN)
    excluded: bool
    deleted: bool
    author: "PlayerRead"
    game_type: "GameTypeRead"
    game_category: "QnACategoryRead"
    question: Optional["QuestionRead"] = None
    prev_version_id: Optional[int] = None
