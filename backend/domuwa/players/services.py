import logging

from domuwa.core.services import CommonServices
from domuwa.players.models import Player
from domuwa.players.schemas import PlayerCreate, PlayerUpdate


class PlayerServices(CommonServices[PlayerCreate, PlayerUpdate, Player]):
    db_model_type = Player
    logger = logging.getLogger(__name__)
