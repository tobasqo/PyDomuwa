from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from domuwa.users.constants import MAX_USERNAME_LEN, MIN_USERNAME_LEN

if TYPE_CHECKING:
    from domuwa.players.models import Player


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: int | None = Field(None, primary_key=True)
    username: str = Field(
        min_length=MIN_USERNAME_LEN,
        max_length=MAX_USERNAME_LEN,
        unique=True,
    )
    is_active: bool = True
    is_staff: bool = False
    hashed_password: str

    player: Optional["Player"] = Relationship(back_populates="user")
