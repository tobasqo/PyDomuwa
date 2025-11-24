import logging
from typing import Sequence

from sqlmodel import Session, select
from typing_extensions import override

from domuwa.core.services import CommonServices
from domuwa.questions.models import Question
from domuwa.questions.schemas import QuestionCreate, QuestionUpdate


class QuestionServices(CommonServices[QuestionCreate, QuestionUpdate, Question]):
    db_model_type = Question
    logger = logging.getLogger(__name__)

    @override
    async def get_all(
        self,
        session: Session,
        offset: int = 0,
        limit: int = 25,
        include_deleted: bool = False,
    ) -> Sequence[Question]:
        stmt = select(self.db_model_type)

        if not include_deleted:
            stmt = stmt.where(Question.deleted == False)  # noqa: E712

        stmt = stmt.offset(offset).limit(limit).order_by(Question.excluded)  # type: ignore
        return session.exec(stmt).all()

    @override
    async def update(
        self,
        model: Question,
        model_update: QuestionUpdate,
        session: Session,
    ):
        update_data = model_update.model_dump(exclude_unset=True)
        model_data = model.model_dump(exclude={"id"}) | update_data
        updated_model = Question(**model_data)

        updated_model.prev_version = model
        model.next_versions.append(updated_model)

        answers = model.answers
        if answers:
            updated_model.answers = answers

        session.add(updated_model)
        session.add(model)
        session.commit()
        session.refresh(updated_model)
        return updated_model

    @override
    async def save(
        self,
        model: QuestionCreate | Question,
        session: Session,
    ) -> Question:
        from domuwa.game_types.services import GameTypeServices
        from domuwa.qna_categories.services import QnACategoryServices

        assert model.game_category_id is not None
        await self.find_related_model(
            model.game_category_id, QnACategoryServices(), session
        )
        assert model.game_type_id is not None
        await self.find_related_model(model.game_type_id, GameTypeServices(), session)
        return await super().save(model, session)

    @override
    async def delete(self, model: Question, session: Session):
        model.deleted = True

        for answer in model.answers:
            answer.deleted = True
            session.add(answer)

        session.add(model)
        session.commit()
        self.logger.debug("marked %s(id=%d) as deleted", Question.__name__, model.id)
