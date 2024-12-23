import logging

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from domuwa.auth.models import User, UserCreate, UserDb, UserUpdate

logger = logging.getLogger(__name__)


async def save_user(user: User, session: Session):
    if not isinstance(user, UserDb):
        user = UserDb.model_validate(user)
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
    return session.exec(select(UserDb).where(UserDb.login == username)).first()  # type: ignore


async def get_by_id(user_id: int, session: Session):
    return session.exec(select(UserDb).where(UserDb.id == user_id)).first()


async def get_all(session: Session):
    return session.exec(select(UserDb)).all()


async def create(user: UserCreate, session: Session):
    return await save_user(user, session)


async def update(user: UserDb, user_update: UserUpdate, session: Session):
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    return await save_user(user, session)


async def delete(user: UserDb, session: Session):
    user.is_active = False
    session.add(user)
    session.commit()
    logger.debug("marked %s(id=%d) as inactive", User.__name__, user.id)
