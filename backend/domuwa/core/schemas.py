from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class APISchemaModel(BaseModel):
    model_config = ConfigDict(
        # from_attributes=True,
        populate_by_name=True,
        # alias_generator=AliasGenerator(
        #     validation_alias=to_snake, serialization_alias=to_camel
        # ),
        alias_generator=to_camel,
    )


class APISchemaResponseModel(APISchemaModel):
    id: int
