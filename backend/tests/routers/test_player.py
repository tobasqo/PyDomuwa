from typing import TYPE_CHECKING

from fastapi import status
from fastapi.testclient import TestClient
from typing_extensions import override

from domuwa.models import Player
from domuwa.services.players_services import PlayerServices
from tests.factories import PlayerFactory, UserFactory
from tests.routers import CommonTestCase

if TYPE_CHECKING:
    from domuwa.auth import User


class TestPlayer(CommonTestCase[Player]):
    path = "/api/players/"
    services = PlayerServices()

    @override
    def assert_valid_response(self, response_data: dict) -> None:
        assert "id" in response_data, response_data
        assert "games_played" in response_data, response_data
        assert "games_won" in response_data, response_data

    @override
    def assert_valid_response_values(
        self,
        response_data: dict,
        model: Player,
    ) -> None:
        assert response_data["id"] == model.id
        assert response_data["games_played"] == model.games_played
        assert response_data["games_won"] == model.games_won

    @override
    def build_model(self) -> Player:
        user: User = UserFactory.create()
        return PlayerFactory.build(id=user.id)

    @override
    def create_model(self) -> Player:
        user: User = UserFactory.create()
        return PlayerFactory.create(id=user.id)

    @override
    def test_update(
        self,
        api_client: TestClient,
        authorization_headers: dict[str, str],
    ):
        user: User = UserFactory.create()
        player: Player = PlayerFactory.create(id=user.id)

        response = api_client.patch(
            f"{self.path}{player.id}",
            json={"games_won": 1},
            headers=authorization_headers,
        )
        assert response.status_code == status.HTTP_200_OK, response.text
        response_data = response.json()
        self.assert_valid_response(response_data)

        response = api_client.get(
            f"{self.path}{player.id}",
            headers=authorization_headers,
        )
        assert response.status_code == status.HTTP_200_OK, response.text
        response_data = response.json()
        self.assert_valid_response(response_data)
        assert response_data["games_won"] == 1
