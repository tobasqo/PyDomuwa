import logging
from typing import Sequence

from sqlmodel import Session, select
from typing_extensions import override

from domuwa.answers.models import Answer
from domuwa.answers.schemas import AnswerCreate, AnswerUpdate
from domuwa.core.services import CommonServices


class AnswerServices(CommonServices[AnswerCreate, AnswerUpdate, Answer]):
    db_model_type = Answer
    logger = logging.getLogger(__name__)

    @override
    async def get_all(
        self,
        session: Session,
        offset: int = 0,
        limit: int = 25,
        include_deleted: bool = False,
    ) -> Sequence[Answer]:
        stmt = select(self.db_model_type)

        if not include_deleted:
            stmt = stmt.where(Answer.deleted == False)  # noqa: E712

        stmt = stmt.offset(offset).limit(limit).order_by(Answer.excluded)  # type: ignore
        return session.exec(stmt).all()

    @override
    async def update(
        self,
        model: Answer,
        model_update: AnswerUpdate,
        session: Session,
    ):
        update_data = model_update.model_dump(exclude_unset=True)
        model_data = model.model_dump(exclude={"id"}) | update_data
        updated_model = Answer(**model_data)

        updated_model.prev_version = model
        model.next_versions.append(updated_model)

        question = model.question
        if question is not None:
            question.answers.remove(model)
            question.answers.append(updated_model)
            session.add(question)

        session.add(updated_model)
        session.add(model)
        session.commit()
        session.refresh(updated_model)
        return updated_model

    @override
    async def delete(self, model: Answer, session: Session):
        model.deleted = True
        session.add(model)
        session.commit()
        self.logger.debug("marked %s(id=%d) as deleted", Answer.__name__, model.id)  # type: ignore
