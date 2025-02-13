from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from domuwa.models import Player

MIN_USERNAME_LEN = 4
MAX_USERNAME_LEN = 32
MIN_PASSWORD_LEN = 8
MAX_PASSWORD_LEN = 40


class Token(SQLModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(SQLModel):
    username: str | None = None


class UserBase(SQLModel):
    username: str
    is_active: bool = True
    is_staff: bool = False


class UserCreate(UserBase):
    username: str = Field(min_length=MIN_USERNAME_LEN, max_length=MAX_USERNAME_LEN)
    password: str = Field(min_length=MIN_PASSWORD_LEN, max_length=MAX_PASSWORD_LEN)


class UserUpdate(SQLModel):
    username: str | None = None
    is_active: bool | None = None
    is_staff: bool | None = None
    password: str | None = Field(
        None,
        min_length=MIN_PASSWORD_LEN,
        max_length=MAX_PASSWORD_LEN,
    )


class User(UserBase, table=True):
    __tablename__ = "user"

    id: int | None = Field(None, primary_key=True)
    username: str = Field(
        min_length=MIN_USERNAME_LEN,
        max_length=MAX_USERNAME_LEN,
        unique=True,
    )
    hashed_password: str

    player: Optional["Player"] = Relationship(back_populates="user")


class UserRead(UserBase):
    id: int
