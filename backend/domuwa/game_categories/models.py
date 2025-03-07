from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from domuwa.game_categories.constants import GameCategoryChoices

if TYPE_CHECKING:
    from domuwa.game_rooms.models import GameRoom


class GameCategory(SQLModel, table=True):
    __tablename__ = "game_category"

    id: int | None = Field(None, primary_key=True)
    name: GameCategoryChoices = Field(index=True, unique=True)

    game_rooms: list["GameRoom"] = Relationship(back_populates="game_category")
