import logging
from abc import ABC, abstractmethod
from typing import Annotated, Generic, final

from fastapi import APIRouter, Depends, status
from sqlmodel import SQLModel, Session
from starlette.responses import Response

from domuwa import auth
from domuwa.auth import User
from domuwa.database import get_db_session
from domuwa.exceptions import (
    InvalidModelInputError,
    InvalidRequestBodyHttpException,
    ModelNotFoundError,
    ModelNotFoundHttpException,
)
from domuwa.services import (
    CommonServices,
    CreateModelT,
    DbModelT,
    UpdateModelT,
)


class CommonRouter(ABC, Generic[CreateModelT, UpdateModelT, DbModelT]):
    prefix: str
    tags: list[str]
    router: APIRouter
    response_model: type[SQLModel]
    services: CommonServices[CreateModelT, UpdateModelT, DbModelT]
    logger: logging.Logger
    db_model_type_name: str
    _lookup = "{model_id}"

    def __init__(self) -> None:
        super().__init__()

        self.router.add_api_route(
            "/",
            self.create,
            status_code=status.HTTP_201_CREATED,
            methods=["POST"],
            response_model=self.response_model,
        )
        self.router.add_api_route(
            "/",
            self.get_all,
            methods=["GET"],
            response_model=list[self.response_model],  # type: ignore
        )
        self.router.add_api_route(
            f"/{self._lookup}",
            self.get_by_id,
            methods=["GET"],
            response_model=self.response_model,
        )
        self.router.add_api_route(
            f"/{self._lookup}",
            self.update,
            response_model=self.response_model,
            methods=["PATCH"],
        )
        self.router.add_api_route(
            f"/{self._lookup}",
            self.delete,
            status_code=status.HTTP_204_NO_CONTENT,
            methods=["DELETE"],
            response_class=Response,
        )

    @final
    async def get_instance(
        self,
        model_id: int,
        session: Session = Depends(get_db_session),
    ) -> DbModelT:
        try:
            return await self.services.get_by_id(model_id, session)
        except ModelNotFoundError as exc:
            err_msg = f"{self.db_model_type_name}(id={model_id}) not found"
            self.logger.warning(err_msg)
            raise ModelNotFoundHttpException(err_msg) from exc

    async def get_by_id(
        self,
        model_id: int,
        session: Annotated[Session, Depends(get_db_session)],
        _: Annotated[User, Depends(auth.get_current_active_user)],
    ):
        return await self.get_instance(model_id, session)

    async def get_all(
        self,
        session: Annotated[Session, Depends(get_db_session)],
        _: Annotated[User, Depends(auth.get_current_active_user)],
        page: int = 0,
        page_size: int = 25,
    ):
        offset = page * page_size
        return await self.services.get_all(session, offset, page_size)

    @abstractmethod
    async def create(
        self,
        model: CreateModelT,
        session: Annotated[Session, Depends(get_db_session)],
        user: Annotated[User, Depends(auth.get_current_active_user)],
    ):
        self.logger.debug(
            "got %s(%s) to create",
            self.db_model_type_name,
            model,
        )
        try:
            return await self.services.create(model, session)
        except InvalidModelInputError as exc:
            err_msg = f"{self.db_model_type_name} cannot be created: {exc}"
            self.logger.warning(err_msg)
            raise InvalidRequestBodyHttpException(err_msg) from exc

    @abstractmethod
    async def update(
        self,
        model_id: int,
        model_update: UpdateModelT,
        session: Annotated[Session, Depends(get_db_session)],
        user: Annotated[User, Depends(auth.get_current_active_user)],
    ):
        self.logger.debug(
            "got %s(%s) to update %s(id=%d)",
            self.db_model_type_name,
            model_update,
            self.db_model_type_name,
            model_id,  # type: ignore
        )
        model = await self.get_instance(model_id, session)
        try:
            return await self.services.update(model, model_update, session)
        except InvalidModelInputError as exc:
            err_msg = (
                f"{self.db_model_type_name}(id={model_id}) cannot be updated: {exc}"
            )
            self.logger.warning(err_msg)
            raise InvalidRequestBodyHttpException(err_msg) from exc

    async def delete(
        self,
        model_id: int,
        session: Annotated[Session, Depends(get_db_session)],
        _: Annotated[User, Depends(auth.get_current_active_user)],
    ):
        self.logger.debug(
            "got %s(id=%d) to delete",
            self.db_model_type_name,
            model_id,
        )
        model = await self.get_instance(model_id, session)
        return await self.services.delete(model, session)
