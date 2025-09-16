import logging
from typing import Any

from sqlmodel import Session, select
from typing_extensions import override

from domuwa.auth.security import get_password_hash
from domuwa.core.exceptions import InvalidModelInputError
from domuwa.core.services import CommonServices
from domuwa.players.schemas import PlayerCreate
from domuwa.players.services import PlayerServices
from domuwa.users.models import User
from domuwa.users.schemas import UserCreate, UserUpdate


class UserServices(CommonServices[UserCreate, UserUpdate, User]):
    db_model_type = User
    logger = logging.getLogger(__name__)

    async def get_by_username(self, username: str, session: Session):
        return session.exec(
            select(self.db_model_type).where(self.db_model_type.username == username)
        ).first()  # type: ignore

    @override
    async def create(self, model: UserCreate, session: Session) -> User:
        user = await self.get_by_username(model.username, session)
        if user is not None:
            err_msg = f"{self.db_model_type.__name__}(username={model.username}) already exists"
            self.logger.error(err_msg)
            raise InvalidModelInputError(err_msg)

        user = self.db_model_type.model_validate(
            model,
            update={"hashed_password": get_password_hash(model.password)},
        )
        user = await self.save(user, session)
        assert user.id is not None
        await PlayerServices().create(PlayerCreate(id=user.id), session)
        return user

    @override
    async def update(
        self, model: User, model_update: UserUpdate, session: Session
    ) -> User:
        update_data = model_update.model_dump(exclude_unset=True)
        extra_data: dict[str, Any] = {}
        if "password" in update_data:
            password = update_data["password"]
            hashed_password = get_password_hash(password)
            extra_data["hashed_password"] = hashed_password
        model.sqlmodel_update(update_data, update=extra_data)
        return await self.save(model, session)

    @override
    async def delete(self, model: User, session: Session):
        model.is_active = False
        session.add(model)
        session.commit()
        self.logger.debug(
            "marked %s(id=%d) as inactive", self.db_model_type.__name__, model.id
        )
