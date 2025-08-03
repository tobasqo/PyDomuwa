import logging

from domuwa import GameCategoryChoices
from domuwa.core.services import CommonServicesForEnumModels
from domuwa.game_categories.models import GameCategory
from domuwa.game_categories.schemas import (
    GameCategoryCreate,
    GameCategoryUpdate,
)


class GameCategoryServices(
    CommonServicesForEnumModels[GameCategoryCreate, GameCategoryUpdate, GameCategory]
):
    db_model_type = GameCategory
    model_create_type = GameCategoryCreate
    choices = GameCategoryChoices
    logger = logging.getLogger(__name__)
