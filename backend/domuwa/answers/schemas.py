from __future__ import annotations

from typing import TYPE_CHECKING

from sqlmodel import Field

from domuwa.answers.constants import TEXT_MAX_LEN, TEXT_MIN_LEN
from domuwa.core.schemas import APISchemaModel, APISchemaResponseModel

if TYPE_CHECKING:
    from domuwa.game_types.schemas import GameTypeRead
    from domuwa.players.schemas import PlayerRead
    from domuwa.qna_categories.schemas import QnACategoryRead


class AnswerCreate(APISchemaModel):
    text: str = Field(min_length=TEXT_MIN_LEN, max_length=TEXT_MAX_LEN)
    author_id: int | None = None
    game_type_id: int
    game_category_id: int
    question_id: int | None = None


class AnswerUpdate(APISchemaModel):
    text: str | None = Field(None, min_length=TEXT_MIN_LEN, max_length=TEXT_MAX_LEN)
    excluded: bool | None = None
    author_id: int | None = None
    game_type_id: int | None = None
    game_category_id: int | None = None
    question_id: int | None = None


class AnswerRead(APISchemaResponseModel):
    text: str | None = Field(None, min_length=TEXT_MIN_LEN, max_length=TEXT_MAX_LEN)
    excluded: bool
    deleted: bool
    author: PlayerRead
    game_type: GameTypeRead
    game_category: QnACategoryRead
    question_id: int | None = None
    prev_version_id: int | None = None
