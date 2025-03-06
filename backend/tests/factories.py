import factory
from factory.alchemy import SQLAlchemyModelFactory

from domuwa.answers.models import Answer
from domuwa.game_categories.models import GameCategory, GameCategoryChoices
from domuwa.game_types.models import GameType, GameTypeChoices
from domuwa.players.models import Player
from domuwa.qna_categories.constants import QnACategoryChoices
from domuwa.qna_categories.models import QnACategory
from domuwa.questions.models import Question
from domuwa.users.models import User


class UserFactory(SQLAlchemyModelFactory):
    username = factory.Sequence(lambda n: f"user{n}")
    is_active = True
    is_staff = False
    hashed_password = "h45h3dp455w0rd"

    class Meta:
        model = User


class GameTypeFactory(SQLAlchemyModelFactory):
    name = GameTypeChoices.EGO

    class Meta:
        model = GameType
        sqlalchemy_get_or_create = ("name",)


class PlayerFactory(SQLAlchemyModelFactory):
    id: int

    class Meta:
        model = Player


class QnACategoryFactory(SQLAlchemyModelFactory):
    name = QnACategoryChoices.SFW

    class Meta:
        model = QnACategory
        sqlalchemy_get_or_create = ("name",)


class AnswerFactory(SQLAlchemyModelFactory):
    text = factory.Sequence(lambda n: "answer text %d" % n)
    excluded: bool = False
    author_id: int
    game_type_id: int
    game_category_id: int
    question_id: int | None = None

    class Meta:
        model = Answer


class QuestionFactory(SQLAlchemyModelFactory):
    text = factory.Sequence(lambda n: "question text %d" % n)
    excluded: bool = False
    deleted: bool = False
    author_id: int
    game_type_id: int
    game_category_id: int

    class Meta:
        model = Question


class GameCategoryFactory(SQLAlchemyModelFactory):
    name = GameCategoryChoices.MIXED

    class Meta:
        model = GameCategory
        sqlalchemy_get_or_create = ("name",)
