import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing_extensions import override

from domuwa import auth
from domuwa.auth import User
from domuwa.database import get_db_session
from domuwa.models.answer import Answer, AnswerCreate, AnswerRead, AnswerUpdate
from domuwa.routers import CommonRouter
from domuwa.services.answers_services import AnswerServices


class AnswerRouter(CommonRouter[AnswerCreate, AnswerUpdate, Answer]):
    prefix = "/answers"
    tags = ["Answer"]
    response_model = AnswerRead
    router = APIRouter(prefix=prefix, tags=tags)  # type: ignore
    services = AnswerServices()
    logger = logging.getLogger(__name__)
    db_model_type_name = Answer.__name__

    def __init__(self) -> None:
        super().__init__()

        self.router.routes.remove(
            next(route for route in self.router.routes if route.name == "create")  # type: ignore
        )
        self.router.add_api_route(
            "/",
            self.create,
            status_code=status.HTTP_201_CREATED,
            methods=["POST"],
            response_model=AnswerRead,
        )

    @override
    async def get_by_id(
        self,
        model_id: int,
        session: Annotated[Session, Depends(get_db_session)],
        user: Annotated[User, Depends(auth.get_current_active_user)],
    ):
        model = await super().get_by_id(model_id, session, user)
        if model.deleted and not user.is_staff:
            err_msg = f"got {self.db_model_type_name}(id={model_id}) to get, but it was deleted"
            self.logger.warning(err_msg)
            raise HTTPException(status.HTTP_404_NOT_FOUND, err_msg)

        return model

    @override
    async def get_all(
        self,
        session: Annotated[Session, Depends(get_db_session)],
        user: Annotated[User, Depends(auth.get_current_active_user)],
        page: int = 0,
        page_size: int = 25,
    ):
        offset = page * page_size
        include_deleted = user.is_staff
        return await self.services.get_all(session, offset, page_size, include_deleted)

    @override
    async def create(
        self,
        model: AnswerCreate,
        session: Annotated[Session, Depends(get_db_session)],
        user: Annotated[User, Depends(auth.get_current_active_user)],
    ):
        model.author_id = user.id
        return await super().create(model, session, user)

    @override
    async def update(
        self,
        model_id: int,
        model_update: AnswerUpdate,
        session: Annotated[Session, Depends(get_db_session)],
        user: Annotated[User, Depends(auth.get_current_active_user)],
    ):
        model_update.author_id = user.id
        return await super().update(model_id, model_update, session, user)


def get_answers_router():
    return AnswerRouter().router
