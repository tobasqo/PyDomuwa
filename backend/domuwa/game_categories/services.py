import logging

from domuwa.core.services import CommonServices
from domuwa.game_categories.models import GameCategory
from domuwa.game_categories.schemas import (
    GameCategoryCreate,
    GameCategoryUpdate,
)


class GameCategoryServices(
    CommonServices[GameCategoryCreate, GameCategoryUpdate, GameCategory]
):
    db_model_type = GameCategory
    logger = logging.getLogger(__name__)
