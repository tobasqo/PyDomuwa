import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing_extensions import override

from domuwa import auth
from domuwa.auth import User
from domuwa.database import get_db_session
from domuwa.models.question import (
    Question,
    QuestionCreate,
    QuestionRead,
    QuestionUpdate,
    QuestionWithAnswersRead,
)
from domuwa.routers import CommonRouter
from domuwa.services.questions_services import QuestionServices


class QuestionRouter(CommonRouter[QuestionCreate, QuestionUpdate, Question]):
    prefix = "/questions"
    tags = ["Question"]
    router = APIRouter(prefix=prefix, tags=tags)  # type: ignore
    response_model = QuestionWithAnswersRead
    services = QuestionServices()
    logger = logging.getLogger(__name__)
    db_model_type_name = Question.__name__

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
            response_model=QuestionRead,
        )

    @override
    async def get_by_id(
        self,
        model_id: int,
        session: Annotated[Session, Depends(get_db_session)],
        user: Annotated[User, Depends(auth.get_current_active_user)],
    ):
        model = await super().get_by_id(model_id, session, user)
        if not model.deleted:
            return model

        err_msg = (
            f"got {self.db_model_type_name}(id={model_id}) to get, but it doesn't exist"
        )
        self.logger.warning(err_msg)
        raise HTTPException(status.HTTP_404_NOT_FOUND, err_msg)

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
