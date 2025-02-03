import logging
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing_extensions import override

from domuwa import auth
from domuwa.auth import User
from domuwa.database import get_db_session
from domuwa.models.player import (
    Player,
    PlayerCreate,
    PlayerRead,
    PlayerUpdate,
)
from domuwa.routers import CommonRouter
from domuwa.services.players_services import PlayerServices


class PlayerRouter(CommonRouter[PlayerCreate, PlayerUpdate, Player]):
    prefix = "/players"
    tags = ["Player"]
    router = APIRouter(prefix=prefix, tags=tags)  # type: ignore
    response_model = PlayerRead
    services = PlayerServices()
    logger = logging.getLogger(__name__)
    db_model_type_name = Player.__name__

    @override
    async def create(
        self,
        model: PlayerCreate,
        session: Annotated[Session, Depends(get_db_session)],
        user: Annotated[User, Depends(auth.get_current_active_user)],
    ):
        return await super().create(model, session, user)

    @override
    async def update(
        self,
        model_id: int,
        model_update: PlayerUpdate,
        session: Annotated[Session, Depends(get_db_session)],
        user: Annotated[User, Depends(auth.get_current_active_user)],
    ):
        return await super().update(model_id, model_update, session, user)


def get_players_router():
    return PlayerRouter().router
