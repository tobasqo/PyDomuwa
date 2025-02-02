import logging
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing_extensions import override

from domuwa import auth
from domuwa.auth import User
from domuwa.database import get_db_session
from domuwa.models import QuestionWithAnswersRead
from domuwa.models.game_type import (
    GameType,
    GameTypeCreate,
    GameTypeRead,
    GameTypeUpdate,
)
from domuwa.routers import CommonRouter400OnSaveError
from domuwa.services.game_type_services import GameTypeServices

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/game-types", tags=["Game Types"])


class GameTypeRouter(
    CommonRouter400OnSaveError[GameTypeCreate, GameTypeUpdate, GameType]
):
    prefix = "/game-types"
    tags = ["Game Type"]
    router = APIRouter(prefix=prefix, tags=tags)  # type: ignore
    response_model = GameTypeRead
    services = GameTypeServices()
    logger = logging.getLogger(__name__)
    db_model_type_name = GameType.__name__

    def __init__(self) -> None:
        super().__init__()

        self.router.add_api_route(
            f"/{self._lookup}/questions",  # type: ignore
            self.get_all_questions,
            methods=["GET"],
            response_model=list[QuestionWithAnswersRead],
        )

    @override
    async def create(
        self,
        model: GameTypeCreate,
        session: Annotated[Session, Depends(get_db_session)],
        admin_user: Annotated[User, Depends(auth.get_admin_user)],
    ):
        return await super().create(model, session, admin_user)

    async def get_all_questions(
        self,
        model_id: int,
        session: Annotated[Session, Depends(get_db_session)],
        _: Annotated[User, Depends(auth.get_current_active_user)],
        page: int = 0,
        page_size: int = 25,
    ):
        questions = await self.services.get_all_questions(
            session,
            model_id,
            page,
            page_size,
        )
        print(questions)
        return questions

    @override
    async def update(
        self,
        model_id: int,
        model_update: GameTypeUpdate,
        session: Annotated[Session, Depends(get_db_session)],
        admin_user: Annotated[User, Depends(auth.get_admin_user)],
    ):
        return await super().update(model_id, model_update, session, admin_user)

    @override
    async def delete(
        self,
        model_id: int,
        session: Annotated[Session, Depends(get_db_session)],
        admin_user: Annotated[User, Depends(auth.get_admin_user)],
    ):
        return await super().delete(model_id, session, admin_user)


def get_game_types_router():
    return GameTypeRouter().router
