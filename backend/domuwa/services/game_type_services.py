import logging
from typing import Sequence

from sqlmodel import Session, select

from domuwa.models import Player, QnACategory, Question
from domuwa.models.game_type import GameType, GameTypeCreate, GameTypeUpdate
from domuwa.services import CommonServices


class GameTypeServices(CommonServices[GameTypeCreate, GameTypeUpdate, GameType]):
    db_model_type = GameType
    logger = logging.getLogger(__name__)

    @staticmethod
    async def get_all_questions(
        session: Session,
        game_type_id: int,
        offset: int = 0,
        page_size: int = 25,
        include_deleted: bool = False,
    ) -> Sequence[Question]:
        stmt = (
            select(Question)
            .join(Player, isouter=True)
            .join(GameType, isouter=True)
            .join(QnACategory, isouter=True)
            .where(Question.game_type_id == game_type_id)  # type: ignore
        )

        if not include_deleted:
            stmt = stmt.where(Question.deleted == False)  # noqa: E712

        stmt = (
            stmt.offset(offset).limit(page_size).order_by(Question.game_category_id)  # type: ignore
        )

        return session.exec(stmt).all()
