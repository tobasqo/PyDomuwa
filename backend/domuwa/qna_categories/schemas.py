from domuwa.core.schemas import APISchemaModel, APISchemaResponseModel
from domuwa.qna_categories.constants import QnACategoryChoices


class QnACategoryBase(APISchemaModel):
    name: QnACategoryChoices


class QnACategoryCreate(QnACategoryBase):
    pass


class QnACategoryUpdate(QnACategoryBase):
    pass


class QnACategoryRead(APISchemaResponseModel, QnACategoryBase):
    pass
