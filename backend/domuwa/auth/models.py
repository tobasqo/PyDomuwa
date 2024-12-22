from sqlmodel import Field, SQLModel


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: str
    scopes: list[str] = Field(default_factory=list)


class User(SQLModel):
    login: str
    email: str | None = None
    is_active: bool | None = None
    is_staff: bool | None = None


class UserDb(User, table=True):
    # TODO: add admin privileges
    __tablename__ = "user"

    id: int | None = Field(None, primary_key=True)
    hashed_password: str
