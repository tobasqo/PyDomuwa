import logging
from abc import ABC
from collections.abc import Sequence
from typing import Generic, TypeVar

from sqlalchemy.exc import IntegrityError
from sqlmodel import SQLModel, Session, select

CreateModelT = TypeVar("CreateModelT", bound=SQLModel)
UpdateModelT = TypeVar("UpdateModelT", bound=SQLModel)
DbModelT = TypeVar("DbModelT", bound=SQLModel)


class CommonServices(ABC, Generic[CreateModelT, UpdateModelT, DbModelT]):
    db_model_type: type[DbModelT]
    logger: logging.Logger

    async def create(self, model: CreateModelT, session: Session) -> DbModelT | None:
        return await self.save(model, session)

    async def get_by_id(self, model_id: int, session: Session) -> DbModelT | None:
        model = session.get(self.db_model_type, model_id)
        if model is None:
            self.logger.warning(
                "%s(id=%d) not found",
                self.db_model_type.__name__,
                model_id,
            )
        return model

    async def get_all(
        self,
        session: Session,
        offset: int = 0,
        limit: int = 25,
    ) -> Sequence[DbModelT]:
        return session.exec(
            select(self.db_model_type).offset(offset).limit(limit)
        ).all()

    async def update(
        self,
        model: DbModelT,
        model_update: UpdateModelT,
        session: Session,
    ) -> DbModelT | None:
        update_data = model_update.model_dump(exclude_unset=True)
        model.sqlmodel_update(update_data)
        return await self.save(model, session)

    async def save(
        self,
        model: CreateModelT | DbModelT,
        session: Session,
    ) -> DbModelT | None:
        if not isinstance(model, self.db_model_type):
            model = self.db_model_type.model_validate(model)
        try:
            session.add(model)
            session.commit()
        except IntegrityError as exc:
            self.logger.error(str(exc))
            return None
        session.refresh(model)
        self.logger.debug("saved %s(%s) to db", model.__class__.__name__, model)
        return model  # type: ignore

    async def delete(self, model: DbModelT, session: Session) -> None:
        session.delete(model)
        session.commit()
        self.logger.debug("removed %s(id=%d)", model.__class__.__name__, model.id)  # type: ignore
