from sqlmodel import SQLModel, Session, create_engine

from domuwa.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},
)


def link_models():
    def get_subclasses(kls: type[SQLModel]):
        for subclass in kls.__subclasses__():
            yield from get_subclasses(subclass)
            yield subclass

    models = get_subclasses(SQLModel)
    for cls in models:
        cls.model_rebuild()


def create_db_and_tables():
    link_models()
    SQLModel.metadata.create_all(engine)


def get_db_session():
    with Session(engine) as db_sess:
        yield db_sess
