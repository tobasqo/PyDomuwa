import logging
from typing import Any

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from domuwa.auth.models import User, UserCreate, UserDb, UserUpdate
from domuwa.auth.security import get_password_hash

logger = logging.getLogger(__name__)


async def save_user(user: User, session: Session):
    try:
        session.add(user)
        session.commit()
    except IntegrityError as exc:
        logger.error(str(exc))
        return None
    session.refresh(user)
    logger.debug("saved %s(%s) to db", User.__name__, user)
    return user


async def get_by_username(username: str, session: Session):
    return session.exec(select(UserDb).where(UserDb.username == username)).first()  # type: ignore


async def get_by_id(user_id: int, session: Session):
    return session.exec(select(UserDb).where(UserDb.id == user_id)).first()


async def get_all(session: Session):
    return session.exec(select(UserDb)).all()


async def create(user_create: UserCreate, session: Session):
    user = await get_by_username(user_create.username, session)
    if user is not None:
        logger.error(
            "%s(username=%s) already exists",
            UserDb.__name__,
            user_create.username,
        )
        return None

    user = UserDb.model_validate(
        user_create,
        update={"hashed_password": get_password_hash(user_create.password)},
    )
    return await save_user(user, session)


async def update(user: UserDb, user_update: UserUpdate, session: Session):
    update_data = user_update.model_dump(exclude_unset=True)
    extra_data: dict[str, Any] = {}
    if "password" in update_data:
        password = update_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    user.sqlmodel_update(update_data, update=extra_data)
    return await save_user(user, session)


async def delete(user: UserDb, session: Session):
    user.is_active = False
    session.add(user)
    session.commit()
    logger.debug("marked %s(id=%d) as inactive", User.__name__, user.id)
