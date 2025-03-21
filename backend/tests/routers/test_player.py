from typing import TYPE_CHECKING

from fastapi import status
from httpx import AsyncClient
from sqlmodel import Session
from typing_extensions import override

from domuwa.players.models import Player
from domuwa.players.services import PlayerServices
from tests.factories import PlayerFactory, UserFactory
from tests.routers import CommonTestCase

if TYPE_CHECKING:
    from domuwa.users.models import User


class TestPlayer(CommonTestCase[Player]):
    path = "/api/players/"
    services = PlayerServices()

    @override
    def assert_valid_response(self, response_data: dict) -> None:
        response_data = self.response_keys_to_snake_case(response_data)
        assert "id" in response_data, response_data
        assert "games_played" in response_data, response_data
        assert "games_won" in response_data, response_data

    @override
    def assert_valid_response_values(
        self,
        response_data: dict,
        model: Player,
    ) -> None:
        response_data = self.response_keys_to_snake_case(response_data)
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
    async def test_create(
        self,
        api_client: AsyncClient,
        authorization_headers: dict[str, str],
        db_session: Session,
        *args,
        **kwargs,
    ):
        model = self.build_model()

        response = await api_client.post(
            self.path,
            json=model.model_dump(),
            headers=authorization_headers,
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN, response.text

    async def test_create_as_admin(
        self,
        api_client: AsyncClient,
        admin_authorization_headers: dict[str, str],
        db_session: Session,
    ):
        await super().test_create(api_client, admin_authorization_headers, db_session)

    @override
    async def test_get_all(
        self,
        api_client: AsyncClient,
        authorization_headers: dict[str, str],
        model_count: int = 2,
        *args,
        **kwargs,
    ):
        for _ in range(model_count):
            self.create_model()

        response = await api_client.get(self.path, headers=authorization_headers)
        assert response.status_code == status.HTTP_200_OK, response.text
        response_data = response.json()

        assert isinstance(response_data, list), response_data
        assert len(response_data) == model_count + 1, response_data
        for model_data in response_data:
            self.assert_valid_response(model_data)

    @override
    async def test_update(
        self,
        api_client: AsyncClient,
        authorization_headers: dict[str, str],
        *args,
        **kwargs,
    ):
        user: User = UserFactory.create()
        player: Player = PlayerFactory.create(id=user.id)

        response = await api_client.patch(
            f"{self.path}{player.id}",
            json={"games_won": 1},
            headers=authorization_headers,
        )
        assert response.status_code == status.HTTP_200_OK, response.text
        response_data = response.json()
        self.assert_valid_response(response_data)

        response = await api_client.get(
            f"{self.path}{player.id}",
            headers=authorization_headers,
        )
        assert response.status_code == status.HTTP_200_OK, response.text
        response_data = response.json()
        self.assert_valid_response(response_data)
        assert response_data["gamesWon"] == 1
