import logging

from domuwa.core.services import CommonServicesForEnumModels
from domuwa.qna_categories.models import QnACategory, QnACategoryChoices
from domuwa.qna_categories.schemas import QnACategoryCreate, QnACategoryUpdate


class QnACategoryServices(
    CommonServicesForEnumModels[QnACategoryCreate, QnACategoryUpdate, QnACategory]
):
    db_model_type = QnACategory
    model_create_type = QnACategoryCreate
    choices = QnACategoryChoices
    logger = logging.getLogger(__name__)
