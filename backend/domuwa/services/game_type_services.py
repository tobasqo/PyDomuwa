import logging

from sqlmodel import Session, select

from domuwa.models import Question
from domuwa.models.game_type import GameType, GameTypeCreate, GameTypeUpdate
from domuwa.services import CommonServices


class GameTypeServices(CommonServices[GameTypeCreate, GameTypeUpdate, GameType]):
    db_model_type = GameType
    logger = logging.getLogger(__name__)

    async def get_all_questions(
        self,
        session: Session,
        game_type_id: int,
        page: int = 0,
        page_size: int = 25,
    ):
        offset = page * page_size
        stmt = (
            select(Question)
            .where(Question.game_type_id == game_type_id)
            .offset(offset)
            .limit(page_size)
            .order_by(self.db_model_type.game_category_id)  # type: ignore
        )
        return session.exec(stmt).all()
