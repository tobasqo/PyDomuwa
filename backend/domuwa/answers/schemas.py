from typing import TYPE_CHECKING, Optional

from sqlmodel import Field

from domuwa.answers.constants import TEXT_MAX_LEN, TEXT_MIN_LEN
from domuwa.core.schemas import APISchemaModel, APISchemaResponseModel

if TYPE_CHECKING:
    from domuwa.game_types.schemas import GameTypeRead
    from domuwa.players.schemas import PlayerRead
    from domuwa.qna_categories.schemas import QnACategoryRead
    from domuwa.questions.schemas import QuestionRead


class AnswerBase(APISchemaModel):
    text: str = Field(min_length=TEXT_MIN_LEN, max_length=TEXT_MAX_LEN)
    author_id: int
    game_type_id: int
    game_category_id: int
    question_id: int | None = None


class AnswerCreate(AnswerBase):
    pass


class AnswerUpdate(APISchemaModel):
    text: str | None = Field(None, min_length=TEXT_MIN_LEN, max_length=TEXT_MAX_LEN)
    excluded: bool | None = None
    author_id: int | None = None
    game_type_id: int | None = None
    game_category_id: int | None = None
    question_id: int | None = None


class AnswerRead(APISchemaResponseModel):
    excluded: bool
    deleted: bool
    author: "PlayerRead"
    game_type: "GameTypeRead"
    game_category: "QnACategoryRead"
    question: Optional["QuestionRead"] = None
    prev_version_id: Optional[int] = None
