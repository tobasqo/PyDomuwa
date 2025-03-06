from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from domuwa.core.models import BaseDBModel
from domuwa.game_categories.constants import GameCategoryChoices

if TYPE_CHECKING:
    from domuwa.game_rooms.models import GameRoom


class GameCategory(BaseDBModel):
    __tablename__ = "game_category"

    name: GameCategoryChoices = Field(index=True, unique=True)

    game_rooms: list["GameRoom"] = Relationship(back_populates="game_category")
