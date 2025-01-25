import logging
import warnings

import pytest
from factory.alchemy import SQLAlchemyModelFactory
from fastapi.testclient import TestClient
from main import app
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool

from domuwa import database as db
from domuwa.auth.models import UserCreate
from domuwa.auth.services import create as create_user

logging.getLogger("faker").setLevel(logging.INFO)
logging.getLogger("factory").setLevel(logging.INFO)
logging.getLogger("asyncio").setLevel(logging.INFO)

warnings.filterwarnings(action="ignore", category=DeprecationWarning)

# SQLALCHEMY_DATABASE_URL = "sqlite:///test_database.db"
SQLALCHEMY_DATABASE_URL = "sqlite://"


@pytest.fixture(name="db_session")
def db_session_fixture():
    from tests import factories  # noqa: F401

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    db_sess = Session(engine)

    for factory in SQLAlchemyModelFactory.__subclasses__():
        factory._meta.sqlalchemy_session = db_sess  # type: ignore

    yield db_sess

    db_sess.rollback()
    db_sess.close()


@pytest.fixture(name="api_client")
def api_client_fixture(db_session: Session):
    def override_get_db_session():
        return db_session

    app.dependency_overrides[db.get_db_session] = override_get_db_session

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture(name="test_user")
async def user_fixture(db_session: Session):
    username = "user"
    password = "<PASSWORD>"
    user_data = {"username": username, "password": password}
    await create_user(UserCreate(**user_data), db_session)
    return user_data
