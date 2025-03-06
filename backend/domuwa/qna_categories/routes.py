import logging
from typing import Annotated

from fastapi import Depends
from fastapi.routing import APIRouter
from sqlmodel import Session
from typing_extensions import override

from domuwa import auth
from domuwa.auth import User
from domuwa.core.routes import CommonRouterWithAuth
from domuwa.database import get_db_session
from domuwa.qna_categories.models import QnACategory
from domuwa.qna_categories.schemas import (
    QnACategoryCreate,
    QnACategoryRead,
    QnACategoryUpdate,
)
from domuwa.qna_categories.services import QnACategoryServices


class QnACategoriesRouter(
    CommonRouterWithAuth[QnACategoryCreate, QnACategoryUpdate, QnACategory]
):
    prefix = "/qna-categories"
    tags = ["QnA Category"]
    router = APIRouter(prefix=prefix, tags=tags)  # type: ignore
    response_model = QnACategoryRead
    services = QnACategoryServices()
    logger = logging.getLogger(__name__)
    db_model_type_name = QnACategory.__name__

    @override
    async def create(
        self,
        model: QnACategoryCreate,
        session: Annotated[Session, Depends(get_db_session)],
        admin_user: Annotated[User, Depends(auth.get_admin_user)],
    ):
        return await super().create(model, session, admin_user)

    @override
    async def update(
        self,
        model_id: int,
        model_update: QnACategoryUpdate,
        session: Annotated[Session, Depends(get_db_session)],
        admin_user: Annotated[User, Depends(auth.get_admin_user)],
    ):
        return await super().update(model_id, model_update, session, admin_user)

    @override
    async def delete(
        self,
        model_id: int,
        session: Annotated[Session, Depends(get_db_session)],
        admin_user: Annotated[User, Depends(auth.get_admin_user)],
    ):
        return await super().delete(model_id, session, admin_user)


def get_qna_categories_router():
    return QnACategoriesRouter().router
