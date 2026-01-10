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

        # TODO: add grouping by excluded
        stmt = stmt.offset(offset).limit(limit).order_by(Answer.excluded)  # type: ignore
        return session.exec(stmt).all()

    @override
    async def update(
        self,
        model: Answer,
        model_update: AnswerUpdate,
        session: Session,
    ):
        if model_update.excluded is not None and model.excluded != model_update.excluded:
            model.excluded = model_update.excluded
            session.add(model)
            session.refresh(model)
            return model

        session.autoflush = False

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
        session.autoflush = True
        return updated_model

    @override
    async def save(
        self,
        model: AnswerCreate | Answer,
        session: Session,
    ) -> Answer:
        from domuwa.game_types.services import GameTypeServices
        from domuwa.qna_categories.services import QnACategoryServices
        from domuwa.questions.services import QuestionServices

        assert model.game_category_id is not None
        await self.find_related_model(
            model.game_category_id, QnACategoryServices(), session
        )
        assert model.game_type_id is not None
        await self.find_related_model(model.game_type_id, GameTypeServices(), session)
        if model.question_id is not None:
            await self.find_related_model(
                model.question_id, QuestionServices(), session
            )
        return await super().save(model, session)

    @override
    async def delete(self, model: Answer, session: Session):
        model.deleted = True
        session.add(model)
        session.commit()
        self.logger.debug("marked %s(id=%d) as deleted", Answer.__name__, model.id)  # type: ignore
