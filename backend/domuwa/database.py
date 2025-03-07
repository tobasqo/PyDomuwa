from sqlalchemy import Engine
from sqlmodel import SQLModel, Session, create_engine

from domuwa.answers.models import *  # noqa: F403, F406
from domuwa.config import settings
from domuwa.game_categories.models import *  # noqa: F403, F811
from domuwa.game_rooms.models import *  # noqa: F403, F811
from domuwa.game_types.models import *  # noqa: F403, F811
from domuwa.players.models import *  # noqa: F403, F811
from domuwa.qna_categories.models import *  # noqa: F403, F811
from domuwa.questions.models import *  # noqa: F403, F811
from domuwa.rankings.models import *  # noqa: F403, F811
from domuwa.users.models import *  # noqa: F401, F403, F811

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},
)


# noinspection PyShadowingNames
def create_db_and_tables(engine: Engine = engine):
    SQLModel.metadata.create_all(engine)


def get_db_session():
    with Session(engine) as db_sess:
        yield db_sess
