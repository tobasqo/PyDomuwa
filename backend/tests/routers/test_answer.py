from typing import TYPE_CHECKING, Any

from fastapi import status
from httpx import AsyncClient
from sqlmodel import Session
from typing_extensions import override

from domuwa.models.answer import Answer
from domuwa.services.answers_services import AnswerServices
from tests.factories import (
    AnswerFactory,
    GameTypeFactory,
    PlayerFactory,
    QnACategoryFactory,
    QuestionFactory,
    UserFactory,
)
from tests.routers import CommonTestCase

if TYPE_CHECKING:
    from domuwa.auth import User
    from domuwa.models import GameType, Player, QnACategory, Question


class TestAnswer(CommonTestCase[Answer]):
    path = "/api/answers/"
    services = AnswerServices()

    @override
    def assert_valid_response(self, response_data: dict[str, Any]):
        assert "id" in response_data, response_data
        assert "text" in response_data, response_data
        assert "excluded" in response_data, response_data
        assert "author" in response_data, response_data
        assert "game_type" in response_data, response_data
        assert "game_category" in response_data, response_data

    # noinspection DuplicatedCode
    @override
    def assert_valid_response_values(
        self,
        response_data: dict,
        model: Answer,
    ) -> None:
        assert response_data["id"] == model.id
        assert response_data["text"] == model.text
        assert response_data["excluded"] == model.excluded
        assert response_data["author"]["id"] == model.author.id  # type: ignore
        assert response_data["game_type"]["id"] == model.game_type.id  # type: ignore
        assert response_data["game_category"]["id"] == model.game_category.id  # type: ignore

    @override
    async def assert_valid_delete(self, model_id: int, db_session: Session) -> None:
        answer = await self.services.get_by_id(model_id, db_session)
        assert answer is not None
        assert answer.deleted

    @override
    def build_model(self) -> Answer:
        game_type: GameType = GameTypeFactory.create()
        game_category: QnACategory = QnACategoryFactory.create()
        return AnswerFactory.build(
            game_type_id=game_type.id,
            game_category_id=game_category.id,
        )

    # noinspection DuplicatedCode
    @staticmethod
    def build_model_with_question() -> Answer:
        user: User = UserFactory.create()
        player: Player = PlayerFactory.create(id=user.id)
        game_type: GameType = GameTypeFactory.create()
        game_category: QnACategory = QnACategoryFactory.create()
        question: Question = QuestionFactory.create(
            author_id=player.id,
            game_type_id=game_type.id,
            game_category_id=game_category.id,
        )
        return AnswerFactory.build(
            game_type_id=game_type.id,
            game_category_id=game_category.id,
            question_id=question.id,
        )

    @override
    def create_model(self) -> Answer:
        user: User = UserFactory.create()
        player: Player = PlayerFactory.create(id=user.id)
        game_type: GameType = GameTypeFactory.create()
        game_category: QnACategory = QnACategoryFactory.create()
        return AnswerFactory.create(
            author_id=player.id,
            game_type_id=game_type.id,
            game_category_id=game_category.id,
        )

    # noinspection DuplicatedCode
    @staticmethod
    def create_model_with_question() -> Answer:
        user: User = UserFactory.create()
        player: Player = PlayerFactory.create(id=user.id)
        game_type: GameType = GameTypeFactory.create()
        game_category: QnACategory = QnACategoryFactory.create()
        question: Question = QuestionFactory.create(
            author_id=player.id,
            game_type_id=game_type.id,
            game_category_id=game_category.id,
        )
        return AnswerFactory.create(
            game_type_id=game_type.id,
            game_category_id=game_category.id,
            question_id=question.id,
        )

    # noinspection DuplicatedCode
    async def test_create_answer_with_question(
        self,
        api_client: AsyncClient,
        authorization_headers: dict[str, str],
        db_session: Session,
    ):
        answer = self.build_model_with_question()

        response = await api_client.post(
            self.path,
            json=answer.model_dump(),
            headers=authorization_headers,
        )
        assert response.status_code == status.HTTP_201_CREATED, response.text
        response_data = response.json()
        self.assert_valid_response(response_data)

        response = await api_client.get(
            f"{self.path}{response_data['id']}",
            headers=authorization_headers,
        )
        assert response.status_code == status.HTTP_200_OK, response.text
        answer_response_data = response.json()
        self.assert_valid_response(answer_response_data)

        db_answer = await self.services.get_by_id(response_data["id"], db_session)
        assert db_answer is not None

        question = db_answer.question
        assert question is not None

        answer_response_data = answer.model_dump(exclude={"id", "author_id"})
        answer_from_db_question_data = question.answers[0].model_dump(
            exclude={"id", "author_id"}
        )
        assert answer_response_data == answer_from_db_question_data, question.answers

    async def test_get_all_deleted_answers(
        self,
        api_client: AsyncClient,
        authorization_headers: dict[str, str],
    ):
        user: User = UserFactory.create()
        player: Player = PlayerFactory.create(id=user.id)
        game_type: GameType = GameTypeFactory.create()
        game_category: QnACategory = QnACategoryFactory.create()
        AnswerFactory.create_batch(
            3,
            game_type_id=game_type.id,
            game_category_id=game_category.id,
            author_id=player.id,
            deleted=True,
        )

        response = await api_client.get(self.path, headers=authorization_headers)
        assert response.status_code == status.HTTP_200_OK, response.text
        response_data = response.json()
        assert len(response_data) == 0, response_data

    async def test_get_all_deleted_answers_as_admin(
        self,
        api_client: AsyncClient,
        admin_authorization_headers: dict[str, str],
    ):
        expected_count = 3
        user: User = UserFactory.create()
        player: Player = PlayerFactory.create(id=user.id)
        game_type: GameType = GameTypeFactory.create()
        game_category: QnACategory = QnACategoryFactory.create()
        AnswerFactory.create_batch(
            expected_count,
            game_type_id=game_type.id,
            game_category_id=game_category.id,
            author_id=player.id,
            deleted=True,
        )

        response = await api_client.get(self.path, headers=admin_authorization_headers)
        assert response.status_code == status.HTTP_200_OK, response.text
        response_data = response.json()
        assert len(response_data) == expected_count, response_data

    # noinspection DuplicatedCode
    @override
    async def test_update(
        self,
        api_client: AsyncClient,
        authorization_headers: dict[str, str],
        *args,
        **kwargs,
    ):
        import warnings

        warnings.filterwarnings("ignore", module="sqlmodel.orm.session")

        answer = self.create_model()
        new_text = "new text"

        response = await api_client.patch(
            f"{self.path}{answer.id}",
            json={"text": new_text},
            headers=authorization_headers,
        )
        assert response.status_code == status.HTTP_200_OK, response.text
        response_data = response.json()
        self.assert_valid_response(response_data)

        assert response_data["id"] >= answer.id, response_data

        assert response_data["text"] != answer.text, response_data
        assert response_data["text"] == new_text, response_data

        assert response_data["excluded"] == answer.excluded, response_data

        assert response_data["author"] is not None, response_data
        assert answer.author is not None
        assert response_data["author"]["id"] != answer.author.id

        assert response_data["game_type"]["id"] == answer.game_type.id, response_data  # type: ignore
        assert response_data["game_type"]["name"] == answer.game_type.name  # type: ignore

        assert (
            response_data["game_category"]["id"] == answer.game_category.id  # type: ignore
        ), response_data
        assert response_data["game_category"]["name"] == answer.game_category.name  # type: ignore

    async def test_delete_answer_with_question(
        self,
        api_client: AsyncClient,
        authorization_headers: dict[str, str],
        db_session: Session,
    ):
        answer = self.create_model_with_question()
        answer_id = answer.id
        assert answer_id is not None

        response = await api_client.delete(
            f"{self.path}{answer_id}",
            headers=authorization_headers,
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT, response.text

        response = await api_client.get(
            f"{self.path}{answer_id}",
            headers=authorization_headers,
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND, response.text

        db_answer = await self.services.get_by_id(answer_id, db_session)
        assert db_answer is not None

        question = db_answer.question
        assert question is not None
        assert not question.deleted
