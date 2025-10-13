from pydantic import AliasGenerator, BaseModel, ConfigDict
from pydantic.alias_generators import to_camel, to_snake


class APISchemaModel(BaseModel):
    model_config = ConfigDict(
        # from_attributes=True,
        populate_by_name=True,
        alias_generator=AliasGenerator(
            alias=to_snake, validation_alias=to_snake, serialization_alias=to_camel
        ),
    )


class APISchemaResponseModel(APISchemaModel):
    id: int
