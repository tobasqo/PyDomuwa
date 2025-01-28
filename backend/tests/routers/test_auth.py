from fastapi import status
from fastapi.testclient import TestClient

from domuwa.auth import services
from domuwa.auth.security import get_password_hash
from tests.factories import UserFactory
from tests.utils import UserData, get_authorization_headers


class TestAuth:
    path = "/auth/"
    services = services

    async def test_login_for_access_token(
        self,
        api_client: TestClient,
        user_data: UserData,
    ):
        response = api_client.post(f"{self.path}login", data=user_data)  # type: ignore
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK, response_data
        assert "access_token" in response_data, response_data
        assert "token_type" in response_data, response_data

    def test_login_for_access_token_non_existing_user(
        self,
        api_client: TestClient,
    ):
        user_data = {"username": "user", "password": "<PASSWORD>"}

        response = api_client.post(f"{self.path}login", data=user_data)
        response_data = response.json()
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, response_data

    def test_read_user(
        self,
        api_client: TestClient,
        authorization_headers: dict[str, str],
    ):
        response = api_client.get(f"{self.path}me", headers=authorization_headers)
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK, response_data
        assert "username" in response_data, response_data

    def test_read_non_existing_user(self, api_client: TestClient):
        response = api_client.get(f"{self.path}me")
        response_data = response.json()
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, response_data

    def test_create_user(self, api_client: TestClient):
        user_data = UserData(username="user", password="<PASSWORD>")

        response = api_client.post(self.path, json=user_data)  # type: ignore
        response_data = response.json()
        assert response.status_code == status.HTTP_201_CREATED, response_data
        assert "username" in response_data, response_data
        assert "is_active" in response_data, response_data
        assert response_data["is_active"] is True, response_data
        assert "is_staff" in response_data, response_data
        assert response_data["is_staff"] is False, response_data

    def test_create_user_existing_username(
        self,
        api_client: TestClient,
        user_data: UserData,
    ):
        response = api_client.post(self.path, json=user_data)  # type: ignore
        response_data = response.json()
        assert response.status_code == status.HTTP_400_BAD_REQUEST, response_data

    def test_get_all_users(
        self,
        api_client: TestClient,
        authorization_headers: dict[str, str],
    ):
        to_create = 3
        UserFactory.create_batch(to_create)
        expected_count = to_create + 1

        response = api_client.get(self.path, headers=authorization_headers)
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK, response_data
        assert len(response_data) == expected_count, response_data

    def test_get_user_by_id(
        self,
        api_client: TestClient,
        authorization_headers: dict[str, str],
    ):
        user = UserFactory.create()

        response = api_client.get(
            f"{self.path}{user.id}",
            headers=authorization_headers,
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK, response_data
        assert "username" in response_data, response_data
        assert "is_active" in response_data, response_data
        assert response_data["is_active"] is True, response_data
        assert "is_staff" in response_data, response_data
        assert response_data["is_staff"] is False, response_data

    def test_get_user_by_invalid_id(
        self,
        api_client: TestClient,
        authorization_headers: dict[str, str],
    ):
        response = api_client.get(f"{self.path}-1", headers=authorization_headers)
        response_data = response.json()
        assert response.status_code == status.HTTP_404_NOT_FOUND, response_data

    def test_update_user(
        self,
        api_client: TestClient,
    ):
        username = "user"
        password = "<PASSWORD>"
        user_data: UserData = {"username": username, "password": password}
        user = UserFactory.create(
            **user_data,
            hashed_password=get_password_hash(password),
        )
        authorization_headers = get_authorization_headers(api_client, user_data)
        update_data = {"username": "new username"}

        # noinspection PyTestUnpassedFixture
        response = api_client.patch(
            f"{self.path}{user.id}",
            json=update_data,
            headers=authorization_headers,
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK, response_data
        assert "username" in response_data, response_data
        assert response_data["username"] == update_data["username"], response_data

    def test_update_other_user(
        self,
        api_client: TestClient,
        authorization_headers: dict[str, str],
    ):
        user = UserFactory.create()
        update_data = {"username": "new username"}

        response = api_client.patch(
            f"{self.path}{user.id}",
            json=update_data,
            headers=authorization_headers,
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_403_FORBIDDEN, response_data

    def test_update_other_user_as_admin(
        self,
        api_client: TestClient,
        admin_authorization_headers: dict[str, str],
    ):
        user = UserFactory.create()
        update_data = {"username": "new username"}

        response = api_client.patch(
            f"{self.path}{user.id}",
            json=update_data,
            headers=admin_authorization_headers,
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK, response_data
        assert "username" in response_data, response_data
        assert response_data["username"] == update_data["username"], response_data

    def test_update_non_existing_user(
        self,
        api_client: TestClient,
        authorization_headers: dict[str, str],
    ):
        response = api_client.patch(
            f"{self.path}-1",
            json={"username": "new username"},
            headers=authorization_headers,
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_404_NOT_FOUND, response_data

    def test_update_user_existing_name(
        self,
        api_client: TestClient,
        user_data: UserData,
    ):
        response = api_client.post(self.path, json=user_data)  # type: ignore
        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text


    def test_delete_user(
        self,
        api_client: TestClient,
        authorization_headers: dict[str, str],
    ):
        user = UserFactory.create()

        response = api_client.delete(
            f"{self.path}{user.id}",
            headers=authorization_headers,
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN, response.json()

    def test_delete_non_existing_user(
        self,
        api_client: TestClient,
        authorization_headers: dict[str, str],
    ):
        response = api_client.delete(f"{self.path}-1", headers=authorization_headers)
        assert response.status_code == status.HTTP_403_FORBIDDEN, response.json()

    def test_delete_user_as_admin(
        self,
        api_client: TestClient,
        admin_authorization_headers: dict[str, str],
    ):
        user = UserFactory.create()

        response = api_client.delete(
            f"{self.path}{user.id}",
            headers=admin_authorization_headers,
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT, response.json()

    def test_delete_non_existing_user_as_admin(
        self,
        api_client: TestClient,
        admin_authorization_headers: dict[str, str],
    ):
        response = api_client.delete(
            f"{self.path}-1",
            headers=admin_authorization_headers,
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND, response.json()
