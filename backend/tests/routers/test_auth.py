from fastapi import status
from httpx import AsyncClient

from domuwa.users.services import UserServices
from tests.utils import UserData


class TestAuth:
    path = "/auth/"
    services = UserServices()

    async def test_login_for_access_token(
        self,
        api_client: AsyncClient,
        user_data: UserData,
    ):
        response = await api_client.post(f"{self.path}token", data=user_data)  # type: ignore
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK, response_data
        assert "accessToken" in response_data, response_data
        assert "tokenType" in response_data, response_data

    async def test_login_for_access_token_non_existing_user(
        self,
        api_client: AsyncClient,
    ):
        user_data = {"username": "user", "password": "<PASSWORD>"}

        response = await api_client.post(f"{self.path}token", data=user_data)
        response_data = response.json()
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, response_data

    async def test_get_current_user(
        self, api_client: AsyncClient, authorization_headers: dict[str, str]
    ):
        response = await api_client.get(f"{self.path}me", headers=authorization_headers)
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK, response_data
        assert "username" in response_data, response_data

    async def test_get_current_user_not_logged_in(self, api_client: AsyncClient):
        response = await api_client.get(f"{self.path}me")
        response_data = response.json()
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, response_data
