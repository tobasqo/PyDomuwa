import logging

from domuwa.core.services import CommonServices
from domuwa.qna_categories.models import QnACategory
from domuwa.qna_categories.schemas import QnACategoryCreate, QnACategoryUpdate


class QnACategoryServices(
    CommonServices[QnACategoryCreate, QnACategoryUpdate, QnACategory]
):
    db_model_type = QnACategory
    logger = logging.getLogger(__name__)
