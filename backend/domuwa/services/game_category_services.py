import logging

from domuwa.models.game_category import (
    GameCategory,
    GameCategoryCreate,
    GameCategoryUpdate,
)
from domuwa.services import CommonServices


class GameCategoryServices(
    CommonServices[GameCategoryCreate, GameCategoryUpdate, GameCategory]
):
    db_model_type = GameCategory
    logger = logging.getLogger(__name__)
