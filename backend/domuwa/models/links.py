from typing import Optional

from sqlmodel import Field, SQLModel


class GameRoomQuestionsLink(SQLModel, table=True):
    __tablename__ = "game_room_questions_links"

    game_room_id: Optional[int] = Field(
        None,
        foreign_key="game_room.id",
        primary_key=True,
    )
    question_id: Optional[int] = Field(
        None,
        foreign_key="question.id",
        primary_key=True,
    )
