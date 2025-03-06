from sqlmodel import Field, SQLModel


class BaseDBModel(SQLModel, table=True):
    id: int | None = Field(None, primary_key=True)
