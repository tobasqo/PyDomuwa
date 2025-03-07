from domuwa.core.schemas import APISchemaModel, APISchemaResponseModel
from domuwa.users.schemas import UserRead


class PlayerBase(APISchemaModel):
    id: int


class PlayerCreate(PlayerBase):
    pass


class PlayerUpdate(APISchemaModel):
    games_played: int | None = None
    games_won: int | None = None


class PlayerRead(APISchemaResponseModel, PlayerBase):
    user: UserRead
    games_played: int
    games_won: int
