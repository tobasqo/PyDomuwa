import logging
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing_extensions import override

from domuwa import auth
from domuwa.auth import User
from domuwa.core.routes import CommonRouterWithAuth
from domuwa.database import get_db_session
from domuwa.game_types.models import GameType
from domuwa.game_types.schemas import (
    GameTypeCreate,
    GameTypeRead,
    GameTypeUpdate,
)
from domuwa.game_types.services import GameTypeServices
from domuwa.questions.schemas import QuestionWithAnswersRead


class GameTypeRoutes(
    CommonRouterWithAuth[GameTypeServices, GameTypeCreate, GameTypeUpdate, GameType]
):
    prefix = "/game-types"
    tags = ["Game Type"]
    router = APIRouter(prefix=prefix, tags=tags)  # type: ignore
    response_model = GameTypeRead
    services = GameTypeServices()
    logger = logging.getLogger(__name__)
    db_model_type_name = GameType.__name__

    @override
    def _init_api_routes(self):
        super()._init_api_routes()
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
        user: Annotated[User, Depends(auth.get_admin_user)],
    ):
        return await super().create(model, session, user)

    async def get_all_questions(
        self,
        model_id: int,
        session: Annotated[Session, Depends(get_db_session)],
        user: Annotated[User, Depends(auth.get_current_active_user)],
        page: int = 1,  # TODO: validate to be gt 0
        page_size: int = 25,
    ):
        offset = (page - 1) * page_size
        include_deleted = user.is_staff
        return await self.services.get_all_questions(
            session, model_id, offset, page_size, include_deleted
        )

    @override
    async def update(
        self,
        model_id: int,
        model_update: GameTypeUpdate,
        session: Annotated[Session, Depends(get_db_session)],
        user: Annotated[User, Depends(auth.get_admin_user)],
    ):
        return await super().update(model_id, model_update, session, user)

    @override
    async def delete(
        self,
        model_id: int,
        session: Annotated[Session, Depends(get_db_session)],
        user: Annotated[User, Depends(auth.get_admin_user)],
    ):
        return await super().delete(model_id, session, user)


def get_game_types_router():
    return GameTypeRoutes().router
