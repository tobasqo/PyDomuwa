from typing import TYPE_CHECKING

from fastapi import status
from httpx import AsyncClient
from sqlmodel import Session
from typing_extensions import override

from domuwa.models.game_type import GameType, GameTypeChoices
from domuwa.services.game_type_services import GameTypeServices
from tests.factories import (
    GameTypeFactory,
    PlayerFactory,
    QnACategoryFactory,
    QuestionFactory,
    UserFactory,
)
from tests.routers import CommonTestCase

if TYPE_CHECKING:
    from domuwa.auth import User
    from domuwa.models import Player, QnACategory


class TestGameType(CommonTestCase[GameType]):
    path = "/api/game-types/"
    services = GameTypeServices()

    @override
    def assert_valid_response(self, response_data: dict) -> None:
        assert "id" in response_data, response_data
        assert "name" in response_data, response_data
        assert (
            response_data["name"] in GameTypeChoices._value2member_map_
        ), response_data

    @override
    def assert_valid_response_values(
        self,
        response_data: dict,
        model: GameType,
    ) -> None:
        assert response_data["id"] == model.id
        assert response_data["name"] == model.name

    @override
    def build_model(self) -> GameType:
        return GameTypeFactory.build()

    @override
    def create_model(self) -> GameType:
        return GameTypeFactory.create()

    @override
    async def test_create(  # type: ignore
        self,
        api_client: AsyncClient,
        admin_authorization_headers: dict[str, str],
        db_session: Session,
        *args,
        **kwargs,
    ):
        return await super().test_create(
            api_client,
            admin_authorization_headers,
            db_session,
        )

    async def test_create_non_admin(
        self,
        api_client: AsyncClient,
        authorization_headers: dict[str, str],
    ):
        model = self.build_model()

        response = await api_client.post(
            self.path,
            json=model.model_dump(),
            headers=authorization_headers,
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN, response.text

    async def test_create_invalid_name(
        self,
        api_client: AsyncClient,
        admin_authorization_headers: dict[str, str],
    ):
        response = await api_client.post(
            self.path,
            json={"name": "not from enum"},
            headers=admin_authorization_headers,
        )
        assert (
            response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        ), response.text

    async def test_create_non_unique_name(
        self,
        api_client: AsyncClient,
        admin_authorization_headers: dict[str, str],
    ):
        game_type: GameType = GameTypeFactory.create()

        response = await api_client.post(
            self.path,
            json={"name": game_type.name},
            headers=admin_authorization_headers,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text

    @override
    async def test_get_all(
        self,
        api_client: AsyncClient,
        authorization_headers: dict[str, str],
        model_count: int = 3,
        *args,
        **kwargs,
    ):
        GameTypeFactory.create(name=GameTypeChoices.EGO)
        GameTypeFactory.create(name=GameTypeChoices.WHOS_MOST_LIKELY)
        GameTypeFactory.create(name=GameTypeChoices.GENTLEMENS_CARDS)

        response = await api_client.get(self.path, headers=authorization_headers)
        assert response.status_code == status.HTTP_200_OK, response.text
        response_data = response.json()

        assert isinstance(response_data, list), response_data
        assert len(response_data) >= 3, response_data

        for game_type in response_data:
            self.assert_valid_response(game_type)

    async def test_get_all_questions(
        self,
        api_client: AsyncClient,
        authorization_headers: dict[str, str],
    ):
        expected_count = 3
        game_type: GameType = GameTypeFactory.create(name=GameTypeChoices.EGO)
        game_category: QnACategory = QnACategoryFactory.create()
        user: User = UserFactory.create()
        player: Player = PlayerFactory.create(id=user.id)
        QuestionFactory.create_batch(
            expected_count,
            game_type_id=game_type.id,
            game_category_id=game_category.id,
            author_id=player.id,
        )

        other_game_type: GameType = GameTypeFactory.create(
            name=GameTypeChoices.WHOS_MOST_LIKELY
        )
        QuestionFactory.create_batch(
            2,
            game_type_id=other_game_type.id,
            game_category_id=game_category.id,
            author_id=player.id,
        )

        response = await api_client.get(
            f"{self.path}{game_type.id}/questions",
            headers=authorization_headers,
        )
        assert response.status_code == status.HTTP_200_OK, response.text
        response_data = response.json()
        assert len(response_data) == expected_count, response_data

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
            2,
            game_type_id=game_type.id,
            game_category_id=game_category.id,
            author_id=player.id,
            deleted=True,
        )

        response = await api_client.get(
            f"{self.path}{game_type.id}/questions",
            headers=authorization_headers,
        )
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

        response = await api_client.get(
            f"{self.path}{game_type.id}/questions",
            headers=admin_authorization_headers,
        )
        assert response.status_code == status.HTTP_200_OK, response.text
        response_data = response.json()
        assert len(response_data) == expected_count, response_data

    @override
    async def test_update(  # type: ignore
        self,
        api_client: AsyncClient,
        admin_authorization_headers: dict[str, str],
        *args,
        **kwargs,
    ):
        game_type: GameType = GameTypeFactory.create(name=GameTypeChoices.EGO)
        updated_game_type_data = {"name": GameTypeChoices.WHOS_MOST_LIKELY}

        response = await api_client.patch(
            f"{self.path}{game_type.id}",
            json=updated_game_type_data,
            headers=admin_authorization_headers,
        )
        assert response.status_code == status.HTTP_200_OK, response.text
        self.assert_valid_response(response.json())

        response = await api_client.get(
            f"{self.path}{game_type.id}",
            headers=admin_authorization_headers,
        )
        assert response.status_code == status.HTTP_200_OK, response.text

        response_data = response.json()
        self.assert_valid_response(response_data)
        assert response_data["name"] == updated_game_type_data["name"], response_data

    async def test_update_non_admin(
        self,
        api_client: AsyncClient,
        authorization_headers: dict[str, str],
    ):
        game_type: GameType = GameTypeFactory.create(name=GameTypeChoices.EGO)
        updated_game_type_data = {"name": GameTypeChoices.WHOS_MOST_LIKELY}

        response = await api_client.patch(
            f"{self.path}{game_type.id}",
            json=updated_game_type_data,
            headers=authorization_headers,
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN, response.text

    async def test_update_invalid_name(
        self,
        api_client: AsyncClient,
        admin_authorization_headers: dict[str, str],
    ):
        game_type: GameType = GameTypeFactory.create()

        response = await api_client.patch(
            f"{self.path}{game_type.id}",
            json={"name": "not from enum"},
            headers=admin_authorization_headers,
        )
        assert (
            response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        ), response.text

    async def test_update_non_unique_name(
        self,
        api_client: AsyncClient,
        admin_authorization_headers: dict[str, str],
    ):
        game_type1: GameType = GameTypeFactory.create(name=GameTypeChoices.EGO)
        game_type2: GameType = GameTypeFactory.create(
            name=GameTypeChoices.WHOS_MOST_LIKELY
        )

        response = await api_client.patch(
            f"{self.path}{game_type1.id}",
            json={"name": game_type2.name},
            headers=admin_authorization_headers,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text

    @override
    async def test_delete(  # type: ignore
        self,
        api_client: AsyncClient,
        admin_authorization_headers: dict[str, str],
        db_session: Session,
        *args,
        **kwargs,
    ):
        return await super().test_delete(
            api_client,
            admin_authorization_headers,
            db_session,
        )
