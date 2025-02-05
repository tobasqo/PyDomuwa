import logging
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing_extensions import override

from domuwa import auth
from domuwa.auth import User
from domuwa.database import get_db_session
from domuwa.models.game_category import (
    GameCategory,
    GameCategoryCreate,
    GameCategoryRead,
    GameCategoryUpdate,
)
from domuwa.routers import CommonRouter
from domuwa.services.game_category_services import GameCategoryServices


class GameCategoryRouter(
    CommonRouter[GameCategoryCreate, GameCategoryUpdate, GameCategory]
):
    prefix = "/game-categories"
    tags = ["Game Category"]
    router = APIRouter(prefix=prefix, tags=tags)  # type: ignore
    response_model = GameCategoryRead
    services = GameCategoryServices()
    logger = logging.getLogger(__name__)
    db_model_type_name = GameCategory.__name__

    @override
    async def create(
        self,
        model: GameCategoryCreate,
        session: Annotated[Session, Depends(get_db_session)],
        admin_user: Annotated[User, Depends(auth.get_admin_user)],
    ):
        return await super().create(model, session, admin_user)

    @override
    async def update(
        self,
        model_id: int,
        model_update: GameCategoryUpdate,
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


def get_game_category_router():
    return GameCategoryRouter().router
