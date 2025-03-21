from typing import TYPE_CHECKING

from fastapi import status
from httpx import AsyncClient
from sqlmodel import Session

from domuwa.questions.models import Question
from domuwa.questions.services import QuestionServices
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
    from domuwa.game_types.models import GameType
    from domuwa.players.models import Player
    from domuwa.qna_categories.models import QnACategory
    from domuwa.users.models import User


class TestQuestion(CommonTestCase[Question]):
    path = "/api/questions/"
    services = QuestionServices()

    def assert_valid_response(self, response_data: dict) -> None:
        response_data = self.response_keys_to_snake_case(response_data)
        assert "id" in response_data, response_data
        assert "text" in response_data, response_data
        assert "excluded" in response_data, response_data
        assert "author" in response_data, response_data
        assert "game_type" in response_data, response_data
        assert "game_category" in response_data, response_data

    # noinspection DuplicatedCode
    def assert_valid_response_values(
        self,
        response_data: dict,
        model: Question,
    ) -> None:
        response_data = self.response_keys_to_snake_case(response_data)
        assert response_data["id"] == model.id
        assert response_data["text"] == model.text
        assert response_data["excluded"] == model.excluded
        assert response_data["author"]["id"] == model.author.id  # type: ignore
        assert response_data["game_type"]["id"] == model.game_type.id  # type: ignore
        assert response_data["game_category"]["id"] == model.game_category.id  # type: ignore

    async def assert_valid_delete(self, model_id: int, db_session: Session) -> None:
        question = await self.services.get_by_id(model_id, db_session)
        assert question is not None
        assert question.deleted
        for answer in question.answers:
            assert answer.deleted

    def build_model(self) -> Question:
        user: User = UserFactory.create()
        author: Player = PlayerFactory.create(id=user.id)
        game_type: GameType = GameTypeFactory.create()
        game_category: QnACategory = QnACategoryFactory.create()
        return QuestionFactory.build(
            author_id=author.id,
            game_type_id=game_type.id,
            game_category_id=game_category.id,
        )

    def create_model(self) -> Question:
        user: User = UserFactory.create()
        author: Player = PlayerFactory.create(id=user.id)
        game_type: GameType = GameTypeFactory.create()
        game_category: QnACategory = QnACategoryFactory.create()
        return QuestionFactory.create(
            author_id=author.id,
            game_type_id=game_type.id,
            game_category_id=game_category.id,
        )

    async def test_get_all_deleted_questions(
        self,
        api_client: AsyncClient,
        authorization_headers: dict[str, str],
    ):
        user: User = UserFactory.create()
        player: Player = PlayerFactory.create(id=user.id)
        game_type: GameType = GameTypeFactory.create()
        game_category: QnACategory = QnACategoryFactory.create()
        QuestionFactory.create_batch(
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

    async def test_get_all_deleted_questions_as_admin(
        self,
        api_client: AsyncClient,
        admin_authorization_headers: dict[str, str],
    ):
        expected_count = 3
        user: User = UserFactory.create()
        player: Player = PlayerFactory.create(id=user.id)
        game_type: GameType = GameTypeFactory.create()
        game_category: QnACategory = QnACategoryFactory.create()
        QuestionFactory.create_batch(
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
    async def test_update(
        self,
        api_client: AsyncClient,
        authorization_headers: dict[str, str],
        *args,
        **kwargs,
    ):
        import warnings

        warnings.filterwarnings("ignore", module="sqlmodel.orm.session")

        question = self.create_model()
        new_text = "new text"

        response = await api_client.patch(
            f"{self.path}{question.id}",
            json={"text": new_text},
            headers=authorization_headers,
        )
        assert response.status_code == status.HTTP_200_OK, response.text
        response_data = self.response_keys_to_snake_case(response.json())
        self.assert_valid_response(response_data)

        assert response_data["id"] >= question.id, response_data

        assert response_data["text"] != question.text, response_data
        assert response_data["text"] == new_text, response_data

        assert response_data["excluded"] == question.excluded, response_data

        assert response_data["author"]["id"] != question.author_id

        assert response_data["game_type"]["id"] == question.game_type.id, response_data  # type: ignore
        assert response_data["game_type"]["name"] == question.game_type.name  # type: ignore

        assert (
            response_data["game_category"]["id"] == question.game_category.id  # type: ignore
        ), response_data
        assert response_data["game_category"]["name"] == question.game_category.name  # type: ignore

    # noinspection DuplicatedCode
    async def test_delete_with_answers(
        self,
        api_client: AsyncClient,
        authorization_headers: dict[str, str],
        db_session: Session,
    ):
        model = self.create_model()
        model_id = model.id
        assert model_id is not None

        AnswerFactory.create_batch(2, question_id=model_id)

        response = await api_client.delete(
            f"{self.path}{model_id}",
            headers=authorization_headers,
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT, response.text

        response = await api_client.get(
            f"{self.path}{model_id}",
            headers=authorization_headers,
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND, response.text

        await self.assert_valid_delete(model_id, db_session)
