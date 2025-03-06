from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from domuwa.core.models import BaseDBModel
from domuwa.qna_categories.constants import QnACategoryChoices

if TYPE_CHECKING:
    from domuwa.answers.models import Answer
    from domuwa.questions.models import Question


class QnACategory(BaseDBModel):
    __tablename__ = "qna_category"

    name: QnACategoryChoices = Field(index=True, unique=True)

    questions: list["Question"] = Relationship(back_populates="game_category")
    answers: list["Answer"] = Relationship(back_populates="game_category")
