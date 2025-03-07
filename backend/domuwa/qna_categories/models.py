from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from domuwa.qna_categories.constants import QnACategoryChoices

if TYPE_CHECKING:
    from domuwa.answers.models import Answer
    from domuwa.questions.models import Question


class QnACategory(SQLModel, table=True):
    __tablename__ = "qna_category"

    id: int | None = Field(None, primary_key=True)
    name: QnACategoryChoices = Field(index=True, unique=True)

    questions: list["Question"] = Relationship(back_populates="game_category")
    answers: list["Answer"] = Relationship(back_populates="game_category")
