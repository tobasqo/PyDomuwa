import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlmodel import Session
from typing_extensions import override

from domuwa import auth
from domuwa.core.routes import CommonRouter
from domuwa.database import get_db_session
from domuwa.users.models import User
from domuwa.users.schemas import UserCreate, UserRead, UserUpdate
from domuwa.users.services import UserServices


class UserRouter(CommonRouter[UserServices, UserCreate, UserUpdate, User]):
    prefix = "/users"
    tags = ["User"]
    router = APIRouter(prefix=prefix, tags=tags)  # type: ignore
    response_model = UserRead
    services = UserServices()
    logger = logging.getLogger(__name__)
    db_model_type_name = User.__name__

    @override
    async def create(
        self, model: UserCreate, session: Annotated[Session, Depends(get_db_session)]
    ):
        return await super().create(model, session)

    @override
    def get_by_id(
        self,
        model_id: int,
        session: Annotated[Session, Depends(get_db_session)],
    ):
        del model_id
        del session
        raise NotImplementedError("Use `get_active_by_id` instead")

    async def get_active_by_id(
        self,
        model_id: int,
        session: Annotated[Session, Depends(get_db_session)],
        _: Annotated[User, Depends(auth.get_current_active_user)],
    ):
        self.logger.debug("got %s(id=%d) to get", User.__name__, model_id)
        user = await self.get_instance(model_id, session)
        if not user.is_active:
            self.logger.warning(
                "got %s(id=%d) to get, but is not active", User.__name__, user.id
            )
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                f"{User.__name__}(id={model_id}) not found)",
            )
        return user

    @override
    def update(
        self,
        model_id: int,
        model_update: UserUpdate,
        session: Annotated[Session, Depends(get_db_session)],
    ):
        del model_id
        del model_update
        del session
        raise NotImplementedError("Use `update_active` instead")

    async def update_active(
        self,
        model_id: int,
        model_update: UserUpdate,
        session: Annotated[Session, Depends(get_db_session)],
        current_user: Annotated[User, Depends(auth.get_current_active_user)],
    ):
        self.logger.debug(
            "got %s(%s) to update %s(id=%d)",
            self.db_model_type_name,
            model_update,
            self.db_model_type_name,
            model_id,
        )
        user = await self.get_instance(model_id, session)
        is_same_user = check_same_user(current_user, user)
        if not (is_same_user or current_user.is_staff):
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                "Not enough permissions",
            )
        return await super().update(model_id, model_update, session)

    @override
    async def delete(
        self,
        model_id: int,
        session: Annotated[Session, Depends(get_db_session)],
    ):
        del model_id
        del session
        raise NotImplementedError("Use `delete_as_admin` instead")

    async def delete_as_admin(
        self,
        model_id: int,
        session: Annotated[Session, Depends(get_db_session)],
        _: Annotated[User, Depends(auth.get_admin_user)],
    ):
        return await super()._delete(model_id, session)

    @override
    def _add_get_by_id_route(self):
        self.router.add_api_route(
            f"/{self._lookup}",
            self.get_active_by_id,
            response_model=UserRead,
        )

    @override
    def _add_update_route(self):
        self.router.add_api_route(
            f"/{self._lookup}",
            self.update_active,
            response_model=UserRead,
            methods=["PATCH"],
        )

    @override
    def _add_delete_route(self):
        self.router.add_api_route(
            f"/{self._lookup}",
            self.delete_as_admin,
            status_code=status.HTTP_204_NO_CONTENT,
            response_class=Response,
            methods=["DELETE"],
        )


def check_same_user(user1: User, user2: User):
    for field in ("id", "username", "hashed_password", "is_active", "is_staff"):
        if getattr(user1, field) != getattr(user2, field):
            return False
    return True


def get_users_router():
    return UserRouter().router
