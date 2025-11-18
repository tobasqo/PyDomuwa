import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing_extensions import override

from domuwa import auth
from domuwa.auth import User
from domuwa.core.routes import CommonRouterWithAuth
from domuwa.database import get_db_session
from domuwa.questions.models import Question
from domuwa.questions.schemas import (
    QuestionCreate,
    QuestionRead,
    QuestionUpdate,
    QuestionWithAnswersRead,
)
from domuwa.questions.services import QuestionServices


class QuestionRouter(
    CommonRouterWithAuth[QuestionServices, QuestionCreate, QuestionUpdate, Question]
):
    prefix = "/questions"
    tags = ["Question"]
    router = APIRouter(prefix=prefix, tags=tags)  # type: ignore
    response_model = QuestionRead
    services = QuestionServices()
    logger = logging.getLogger(__name__)
    db_model_type_name = Question.__name__

    def __init__(self) -> None:
        super().__init__()

        self.router.routes.remove(
            next(route for route in self.router.routes if route.name == "get_by_id")  # type: ignore
        )
        self.router.add_api_route(
            f"/{self._lookup}",
            self.get_by_id,
            status_code=status.HTTP_200_OK,
            methods=["GET"],
            response_model=QuestionWithAnswersRead,
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
        page: int = 1,  # TODO: validate to be gt 0
        page_size: int = 25,
    ):
        offset = (page - 1) * page_size
        include_deleted = user.is_staff
        return await self.services.get_all(session, offset, page_size, include_deleted)

    @override
    async def create(
        self,
        model: QuestionCreate,
        session: Annotated[Session, Depends(get_db_session)],
        user: Annotated[User, Depends(auth.get_current_active_user)],
    ):
        model.author_id = user.id
        return await super().create(model, session, user)

    @override
    async def update(
        self,
        model_id: int,
        model_update: QuestionUpdate,
        session: Annotated[Session, Depends(get_db_session)],
        user: Annotated[User, Depends(auth.get_current_active_user)],
    ):
        model_update.author_id = user.id
        return await super().update(model_id, model_update, session, user)


def get_questions_router():
    return QuestionRouter().router
