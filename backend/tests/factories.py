import factory
from factory.alchemy import SQLAlchemyModelFactory

from domuwa.auth.models import UserDb
from domuwa.models.answer import Answer
from domuwa.models.game_type import GameType, GameTypeChoices
from domuwa.models.player import Player
from domuwa.models.qna_category import QnACategory, QnACategoryChoices
from domuwa.models.question import Question


class UserFactory(SQLAlchemyModelFactory):
    username = factory.Sequence(lambda n: f"user{n}")
    is_active = True
    is_staff = False
    hashed_password = "h45h3dp455w0rd"

    class Meta:
        model = UserDb


class GameTypeFactory(SQLAlchemyModelFactory):
    name = GameTypeChoices.EGO

    class Meta:  # type: ignore
        model = GameType
        sqlalchemy_get_or_create = ("name",)


class PlayerFactory(SQLAlchemyModelFactory):
    name = factory.Sequence(lambda n: "Player %d" % n)

    class Meta:  # type: ignore
        model = Player


class QnACategoryFactory(SQLAlchemyModelFactory):
    name = QnACategoryChoices.SFW

    class Meta:  # type: ignore
        model = QnACategory
        sqlalchemy_get_or_create = ("name",)


class AnswerFactory(SQLAlchemyModelFactory):
    text = factory.Sequence(lambda n: "answer text %d" % n)
    excluded: bool = False
    author_id: int
    game_type_id: int
    game_category_id: int
    question_id: int | None = None

    class Meta:  # type: ignore
        model = Answer


class QuestionFactory(SQLAlchemyModelFactory):
    text = factory.Sequence(lambda n: "question text %d" % n)
    excluded: bool = False
    deleted: bool = False
    author_id: int
    game_type_id: int
    game_category_id: int

    class Meta:  # type: ignore
        model = Question
