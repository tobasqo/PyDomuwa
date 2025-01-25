
from fastapi import status
from fastapi.testclient import TestClient

from domuwa.auth import services


class TestAuth:
    path = "/auth/"
    services = services

    async def test_login_for_access_token(
        self,
        api_client: TestClient,
        test_user: dict[str, str],
    ):
        response = api_client.post(f"{self.path}login", data=test_user)
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK, response_data
        assert "access_token" in response_data, response_data
        assert "token_type" in response_data, response_data
