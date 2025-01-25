from sqlmodel import Field, SQLModel


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: str
    scopes: list[str] = Field(default_factory=list)


class User(SQLModel):
    username: str
    is_active: bool = True
    is_staff: bool = False


class UserCreate(User):
    password: str = Field(min_length=8, max_length=40)


class UserUpdate(SQLModel):
    username: str | None = None
    is_active: bool | None = None
    is_staff: bool | None = None
    password: str | None = Field(None, min_length=8, max_length=40)


class UserDb(User, table=True):
    __tablename__ = "user"

    id: int | None = Field(None, primary_key=True)
    hashed_password: str
