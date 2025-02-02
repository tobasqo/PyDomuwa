import logging
from typing import Any

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from domuwa.auth.models import User, UserBase, UserCreate, UserUpdate
from domuwa.auth.security import get_password_hash
from domuwa.models import PlayerCreate
from domuwa.services.players_services import PlayerServices

logger = logging.getLogger(__name__)


async def save_user(user: UserBase, session: Session):
    try:
        session.add(user)
        session.commit()
    except IntegrityError as exc:
        logger.error(str(exc))
        return None
    session.refresh(user)
    logger.debug("saved %s(%s) to db", UserBase.__name__, user)
    return user


async def get_by_username(username: str, session: Session):
    return session.exec(select(User).where(User.username == username)).first()  # type: ignore


async def get_by_id(user_id: int, session: Session):
    return session.exec(select(User).where(User.id == user_id)).first()  # type: ignore


async def get_all(session: Session):
    return session.exec(select(User)).all()


async def create(user_create: UserCreate, session: Session):
    user = await get_by_username(user_create.username, session)
    if user is not None:
        logger.error(
            "%s(username=%s) already exists",
            User.__name__,
            user_create.username,
        )
        return None

    user = User.model_validate(
        user_create,
        update={"hashed_password": get_password_hash(user_create.password)},
    )
    user = await save_user(user, session)
    await PlayerServices().create(PlayerCreate(id=user.id), session)
    return user


async def update(user: User, user_update: UserUpdate, session: Session):
    update_data = user_update.model_dump(exclude_unset=True)
    extra_data: dict[str, Any] = {}
    if "password" in update_data:
        password = update_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    user.sqlmodel_update(update_data, update=extra_data)
    return await save_user(user, session)


async def delete(user: User, session: Session):
    user.is_active = False
    session.add(user)
    session.commit()
    logger.debug("marked %s(id=%d) as inactive", UserBase.__name__, user.id)
