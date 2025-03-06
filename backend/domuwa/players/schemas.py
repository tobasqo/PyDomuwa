from typing import TYPE_CHECKING

from domuwa.core.schemas import APISchemaModel

if TYPE_CHECKING:
    from domuwa.users.schemas import UserRead


class PlayerBase(APISchemaModel):
    id: int


class PlayerCreate(PlayerBase):
    pass


class PlayerUpdate(APISchemaModel):
    games_played: int | None = None
    games_won: int | None = None


class PlayerRead(PlayerBase):
    user: "UserRead"
    games_played: int
    games_won: int
