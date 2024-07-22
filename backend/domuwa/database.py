from sqlmodel import SQLModel, Session, create_engine

from domuwa.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_db_session():
    with Session(engine) as db_sess:
        yield db_sess
