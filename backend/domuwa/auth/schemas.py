from pydantic import BaseModel

from domuwa.core.schemas import APISchemaModel


class Token(APISchemaModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
