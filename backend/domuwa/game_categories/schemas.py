from domuwa.core.schemas import APISchemaModel, APISchemaResponseModel
from domuwa.game_categories.constants import GameCategoryChoices


class GameCategoryBase(APISchemaModel):
    name: GameCategoryChoices


class GameCategoryCreate(GameCategoryBase):
    pass


class GameCategoryUpdate(GameCategoryBase):
    pass


class GameCategoryRead(APISchemaResponseModel, GameCategoryBase):
    pass
