from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session
from typing_extensions import override

from domuwa.models.game_type import GameType, GameTypeChoices
from domuwa.services.game_type_services import GameTypeServices
from tests.factories import GameTypeFactory
from tests.routers import CommonTestCase


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
    async def test_create(
        self,
        api_client: TestClient,
        admin_authorization_headers: dict[str, str],
        db_session: Session,
    ):
        return await super().test_create(
            api_client, admin_authorization_headers, db_session
        )

    def test_create_non_admin(
        self,
        api_client: TestClient,
        authorization_headers: dict[str, str],
    ):
        model = self.build_model()

        response = api_client.post(
            self.path,
            json=model.model_dump(),
            headers=authorization_headers,
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN, response.text

    def test_create_invalid_name(
        self,
        api_client: TestClient,
        admin_authorization_headers: dict[str, str],
    ):
        response = api_client.post(
            self.path,
            json={"name": "not from enum"},
            headers=admin_authorization_headers,
        )
        assert (
            response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        ), response.text

    def test_create_non_unique_name(
        self,
        api_client: TestClient,
        admin_authorization_headers: dict[str, str],
    ):
        game_type: GameType = GameTypeFactory.create()
        response = api_client.post(
            self.path,
            json={"name": game_type.name},
            headers=admin_authorization_headers,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text

    @override
    def test_get_all(
        self,
        api_client: TestClient,
        authorization_headers: dict[str, str],
        model_count: int = 3,
    ):
        GameTypeFactory.create(name=GameTypeChoices.EGO)
        GameTypeFactory.create(name=GameTypeChoices.WHOS_MOST_LIKELY)
        GameTypeFactory.create(name=GameTypeChoices.GENTLEMENS_CARDS)

        response = api_client.get(self.path, headers=authorization_headers)
        assert response.status_code == status.HTTP_200_OK, response.text
        response_data = response.json()

        assert isinstance(response_data, list), response_data
        assert len(response_data) >= 3, response_data

        for game_type in response_data:
            self.assert_valid_response(game_type)

    @override
    def test_update(
        self,
        api_client: TestClient,
        admin_authorization_headers: dict[str, str],
    ):
        game_type: GameType = GameTypeFactory.create(name=GameTypeChoices.EGO)
        updated_game_type_data = {"name": GameTypeChoices.WHOS_MOST_LIKELY}

        response = api_client.patch(
            f"{self.path}{game_type.id}",
            json=updated_game_type_data,
            headers=admin_authorization_headers,
        )
        assert response.status_code == status.HTTP_200_OK, response.text
        self.assert_valid_response(response.json())

        response = api_client.get(
            f"{self.path}{game_type.id}",
            headers=admin_authorization_headers,
        )
        assert response.status_code == status.HTTP_200_OK, response.text

        response_data = response.json()
        self.assert_valid_response(response_data)
        assert response_data["name"] == updated_game_type_data["name"], response_data

    def test_update_non_admin(
        self,
        api_client: TestClient,
        authorization_headers: dict[str, str],
    ):
        game_type: GameType = GameTypeFactory.create(name=GameTypeChoices.EGO)
        updated_game_type_data = {"name": GameTypeChoices.WHOS_MOST_LIKELY}

        response = api_client.patch(
            f"{self.path}{game_type.id}",
            json=updated_game_type_data,
            headers=authorization_headers,
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN, response.text

    def test_update_invalid_name(
        self,
        api_client: TestClient,
        admin_authorization_headers: dict[str, str],
    ):
        game_type: GameType = GameTypeFactory.create()

        response = api_client.patch(
            f"{self.path}{game_type.id}",
            json={"name": "not from enum"},
            headers=admin_authorization_headers,
        )
        assert (
            response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        ), response.text

    def test_update_non_unique_name(
        self,
        api_client: TestClient,
        admin_authorization_headers: dict[str, str],
    ):
        game_type1: GameType = GameTypeFactory.create(name=GameTypeChoices.EGO)
        game_type2: GameType = GameTypeFactory.create(
            name=GameTypeChoices.WHOS_MOST_LIKELY
        )

        response = api_client.patch(
            f"{self.path}{game_type1.id}",
            json={"name": game_type2.name},
            headers=admin_authorization_headers,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text

    @override
    async def test_delete(
        self,
        api_client: TestClient,
        admin_authorization_headers: dict[str, str],
        db_session: Session,
    ):
        return await super().test_delete(
            api_client,
            admin_authorization_headers,
            db_session,
        )
