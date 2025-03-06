from pydantic import AliasGenerator, ConfigDict
from pydantic.alias_generators import to_camel, to_snake
from sqlmodel import SQLModel


class APISchemaModel(SQLModel):
    model_config = ConfigDict(  # type: ignore
        from_attributes=True,
        populate_by_name=True,
        alias_generator=AliasGenerator(
            validation_alias=to_snake, serialization_alias=to_camel
        ),
    )


class APISchemaResponseModel(APISchemaModel):
    id: int
