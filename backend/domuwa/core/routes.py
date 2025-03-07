import logging
from abc import ABC, abstractmethod
from typing import Annotated, Generic, final

from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from starlette.responses import Response
from typing_extensions import override

from domuwa import auth
from domuwa.auth import User
from domuwa.core.exceptions import (
    InvalidModelInputError,
    InvalidRequestBodyHttpException,
    ModelNotFoundError,
    ModelNotFoundHttpException,
)
from domuwa.core.schemas import APISchemaResponseModel
from domuwa.core.services import (
    CommonServices,
    CreateModelT,
    DbModelT,
    UpdateModelT,
)
from domuwa.database import get_db_session


class BaseRouter(ABC, Generic[CreateModelT, UpdateModelT, DbModelT]):
    prefix: str
    tags: list[str]
    router: APIRouter
    response_model: type[APISchemaResponseModel]
    services: CommonServices[CreateModelT, UpdateModelT, DbModelT]
    logger: logging.Logger
    db_model_type_name: str
    _lookup = "{model_id}"

    def __init__(self) -> None:
        super().__init__()
        self._init_api_routes()

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

    @abstractmethod
    async def get_by_id(self, *args, **kwargs):
        return await self._get_by_id(*args, **kwargs)

    async def _get_by_id(
        self,
        model_id: int,
        session: Annotated[Session, Depends(get_db_session)],
    ):
        return await self.get_instance(model_id, session)

    @abstractmethod
    async def get_all(self, *args, **kwargs):
        return await self._get_all(*args, **kwargs)

    async def _get_all(
        self,
        session: Annotated[Session, Depends(get_db_session)],
        page: int = 0,
        page_size: int = 25,
    ):
        offset = page * page_size
        return await self.services.get_all(session, offset, page_size)

    @abstractmethod
    async def create(self, *args, **kwargs):
        return await self._create(*args, **kwargs)

    async def _create(
        self,
        model: CreateModelT,
        session: Annotated[Session, Depends(get_db_session)],
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
    async def update(self, *args, **kwargs):
        return await self._update(*args, **kwargs)

    async def _update(
        self,
        model_id: int,
        model_update: UpdateModelT,
        session: Annotated[Session, Depends(get_db_session)],
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

    @abstractmethod
    async def delete(self, *args, **kwargs):
        return await self._delete(*args, **kwargs)

    async def _delete(
        self,
        model_id: int,
        session: Annotated[Session, Depends(get_db_session)],
    ):
        self.logger.debug(
            "got %s(id=%d) to delete",
            self.db_model_type_name,
            model_id,
        )
        model = await self.get_instance(model_id, session)
        return await self.services.delete(model, session)

    def _init_api_routes(self):
        self._add_create_route()
        self._add_get_all_route()
        self._add_get_by_id_route()
        self._add_update_route()
        self._add_delete_route()

    def _add_create_route(self):
        self.router.add_api_route(
            "/",
            self.create,
            status_code=status.HTTP_201_CREATED,
            methods=["POST"],
            response_model=self.response_model,
        )

    def _add_get_all_route(self):
        self.router.add_api_route(
            "/",
            self.get_all,
            methods=["GET"],
            response_model=list[self.response_model],  # type: ignore
        )

    def _add_get_by_id_route(self):
        self.router.add_api_route(
            f"/{self._lookup}",
            self.get_by_id,
            methods=["GET"],
            response_model=self.response_model,
        )

    def _add_update_route(self):
        self.router.add_api_route(
            f"/{self._lookup}",
            self.update,
            response_model=self.response_model,
            methods=["PATCH"],
        )

    def _add_delete_route(self):
        self.router.add_api_route(
            f"/{self._lookup}",
            self.delete,
            status_code=status.HTTP_204_NO_CONTENT,
            methods=["DELETE"],
            response_class=Response,
        )


class CommonRouter(BaseRouter[CreateModelT, UpdateModelT, DbModelT]):
    @override
    async def get_by_id(
        self,
        model_id: int,
        session: Annotated[Session, Depends(get_db_session)],
    ):
        return await self._get_by_id(model_id, session)

    @override
    async def get_all(
        self,
        session: Annotated[Session, Depends(get_db_session)],
    ):
        return await self._get_all(session)

    @abstractmethod
    async def create(
        self,
        model: CreateModelT,
        session: Annotated[Session, Depends(get_db_session)],
    ):
        return await self._create(model, session)

    @abstractmethod
    async def update(
        self,
        model_id: int,
        model_update: UpdateModelT,
        session: Annotated[Session, Depends(get_db_session)],
    ):
        return await self._update(model_id, model_update, session)

    async def delete(
        self,
        model_id: int,
        session: Annotated[Session, Depends(get_db_session)],
    ):
        return await self._delete(model_id, session)


class CommonRouterWithAuth(BaseRouter[CreateModelT, UpdateModelT, DbModelT]):
    @override
    async def get_by_id(
        self,
        model_id: int,
        session: Annotated[Session, Depends(get_db_session)],
        _: Annotated[User, Depends(auth.get_current_active_user)],
    ):
        return await self._get_by_id(model_id, session)

    @override
    async def get_all(
        self,
        session: Annotated[Session, Depends(get_db_session)],
        _: Annotated[User, Depends(auth.get_current_active_user)],
    ):
        return await self._get_all(session)

    @abstractmethod
    async def create(
        self,
        model: CreateModelT,
        session: Annotated[Session, Depends(get_db_session)],
        _: Annotated[User, Depends(auth.get_current_active_user)],
    ):
        return await self._create(model, session)

    @abstractmethod
    async def update(
        self,
        model_id: int,
        model_update: UpdateModelT,
        session: Annotated[Session, Depends(get_db_session)],
        _: Annotated[User, Depends(auth.get_current_active_user)],
    ):
        return await self._update(model_id, model_update, session)

    async def delete(
        self,
        model_id: int,
        session: Annotated[Session, Depends(get_db_session)],
        _: Annotated[User, Depends(auth.get_current_active_user)],
    ):
        return await self._delete(model_id, session)
