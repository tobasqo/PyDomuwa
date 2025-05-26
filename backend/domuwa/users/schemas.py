from sqlmodel import Field

from domuwa.core.schemas import APISchemaModel, APISchemaResponseModel
from domuwa.users.constants import (
    MAX_PASSWORD_LEN,
    MAX_USERNAME_LEN,
    MIN_PASSWORD_LEN,
    MIN_USERNAME_LEN,
)


class UserBase(APISchemaModel):
    username: str = Field(min_length=MIN_USERNAME_LEN, max_length=MAX_USERNAME_LEN)


class UserCreate(UserBase):
    password: str = Field(min_length=MIN_PASSWORD_LEN, max_length=MAX_PASSWORD_LEN)


class UserUpdate(APISchemaModel):
    username: str | None = Field(
        None,
        min_length=MIN_USERNAME_LEN,
        max_length=MAX_USERNAME_LEN,
    )
    is_active: bool | None = None
    is_staff: bool | None = None
    password: str | None = Field(
        None,
        min_length=MIN_PASSWORD_LEN,
        max_length=MAX_PASSWORD_LEN,
    )


class UserRead(APISchemaResponseModel, UserBase):
    pass
