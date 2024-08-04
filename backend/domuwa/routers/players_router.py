import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing_extensions import override

from domuwa.database import get_db_session
from domuwa.models.player import (
    Player,
    PlayerCreate,
    PlayerRead,
    PlayerUpdate,
)
from domuwa.routers.common_router import CommonRouter
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
        session: Session = Depends(get_db_session),
    ):
        player = await super().create(model, session)
        if player is None:
            err_msg = f"Cannot create Player({model})."
            self.logger.warning(err_msg)
            raise HTTPException(status.HTTP_400_BAD_REQUEST, err_msg)
        return player

    @override
    async def update(
        self,
        model_id: int,
        model_update: PlayerUpdate,
        session: Session = Depends(get_db_session),
    ):
        db_player = await self.get_instance(model_id, session)
        player_update = await self.services.update(db_player, model_update, session)
        if player_update is None:
            err_msg = (
                f"Cannot update Player(id={model_id}) with Player({model_update})."
            )
            self.logger.warning(err_msg)
            raise HTTPException(status.HTTP_400_BAD_REQUEST, err_msg)
        return player_update


def get_players_router():
    return PlayerRouter().router
