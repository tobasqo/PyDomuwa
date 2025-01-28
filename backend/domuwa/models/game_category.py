from enum import StrEnum
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from domuwa.models.game_room import GameRoom


class GameCategoryChoices(StrEnum):
    SFW = "SFW"
    NSFW = "NSFW"
    MIXED = "Mixed"


class GameCategoryBase(SQLModel):
    name: GameCategoryChoices


class GameCategory(SQLModel, table=True):
    __tablename__ = "game_category"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: GameCategoryChoices = Field(index=True, unique=True)

    game_rooms: list["GameRoom"] = Relationship(back_populates="game_category")


class GameCategoryCreate(GameCategoryBase):
    pass


class GameCategoryUpdate(GameCategoryBase):
    pass


class GameCategoryRead(GameCategoryBase):
    id: int
