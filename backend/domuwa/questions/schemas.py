from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sqlmodel import Field

from domuwa.core.schemas import APISchemaModel, APISchemaResponseModel
from domuwa.questions.constants import TEXT_MAX_LEN, TEXT_MIN_LEN

if TYPE_CHECKING:
    from domuwa.answers.schemas import AnswerRead
    from domuwa.game_types.schemas import GameTypeRead
    from domuwa.players.schemas import PlayerRead
    from domuwa.qna_categories.schemas import QnACategoryRead


class QuestionBase(APISchemaModel):
    text: str = Field(min_length=TEXT_MIN_LEN, max_length=TEXT_MAX_LEN)
    author_id: Optional[int] = None
    game_type_id: int
    game_category_id: int


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(APISchemaModel):
    text: Optional[str] = Field(None, min_length=TEXT_MIN_LEN, max_length=TEXT_MAX_LEN)
    excluded: Optional[bool] = None
    author_id: Optional[int] = None
    game_type_id: Optional[int] = None
    game_category_id: Optional[int] = None


class QuestionRead(APISchemaResponseModel):
    text: str = Field(min_length=TEXT_MIN_LEN, max_length=TEXT_MAX_LEN)
    excluded: bool = False
    deleted: bool = False
    author: PlayerRead
    game_type: GameTypeRead
    game_category: QnACategoryRead
    prev_version_id: Optional[int] = None


class QuestionWithAnswersRead(QuestionRead):
    answers: list[AnswerRead]
