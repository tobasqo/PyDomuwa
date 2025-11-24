import logging
from typing import override

from sqlmodel import Session

from domuwa.core.services import CommonServices
from domuwa.players.models import Player
from domuwa.players.schemas import PlayerCreate, PlayerUpdate


class PlayerServices(CommonServices[PlayerCreate, PlayerUpdate, Player]):
    db_model_type = Player
    logger = logging.getLogger(__name__)

    @override
    async def save(
        self,
        model: PlayerCreate | Player,
        session: Session,
    ) -> Player:
        from domuwa.users.services import UserServices

        await self.find_related_model(model.id, UserServices(), session)
        return await super().save(model, session)
