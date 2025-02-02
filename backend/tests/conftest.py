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
from tests.utils import UserData, get_authorization_headers, get_default_user_data

logging.getLogger("faker").setLevel(logging.INFO)
logging.getLogger("factory").setLevel(logging.INFO)
logging.getLogger("asyncio").setLevel(logging.INFO)
logging.getLogger("python_multipart").setLevel(logging.INFO)
logging.getLogger("passlib").setLevel(logging.ERROR)

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
        factory._meta.sqlalchemy_session_persistence = "commit"

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


@pytest.fixture(name="user_data")
async def user_data_fixture(db_session: Session):
    user_data = get_default_user_data()
    await create_user(UserCreate(**user_data), db_session)
    return user_data


@pytest.fixture(name="inactive_user_data")
async def inactive_user_data_fixture(db_session: Session):
    user_data = get_default_user_data()
    user_data["is_active"] = False
    await create_user(UserCreate(**user_data), db_session)
    return user_data


@pytest.fixture(name="admin_user_data")
async def admin_user_data_fixture(db_session: Session):
    user_data = get_default_user_data()
    user_data["is_staff"] = True
    await create_user(UserCreate(**user_data), db_session)
    return user_data


@pytest.fixture(name="authorization_headers")
async def authorization_headers_fixture(api_client: TestClient, user_data: UserData):
    return get_authorization_headers(api_client, user_data)


@pytest.fixture(name="inactive_authorization_headers")
async def inactive_authorization_headers_fixture(
    api_client: TestClient,
    inactive_user_data: UserData,
):
    return get_authorization_headers(api_client, inactive_user_data)


@pytest.fixture(name="admin_authorization_headers")
async def admin_authorization_headers_fixture(
    api_client: TestClient,
    admin_user_data: UserData,
):
    return get_authorization_headers(api_client, admin_user_data)
