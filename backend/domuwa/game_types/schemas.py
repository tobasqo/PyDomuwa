from domuwa.core.schemas import APISchemaModel, APISchemaResponseModel
from domuwa.game_types.constants import GameTypeChoices


class GameTypeBase(APISchemaModel):
    name: GameTypeChoices


class GameTypeCreate(GameTypeBase):
    pass


class GameTypeUpdate(GameTypeBase):
    pass


class GameTypeRead(APISchemaResponseModel, GameTypeBase):
    pass
