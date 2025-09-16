from fastapi import status
from httpx import AsyncClient
from sqlmodel import Session
from typing_extensions import override

from domuwa.auth.security import get_password_hash
from domuwa.users.models import User
from domuwa.users.services import UserServices
from tests.factories import UserFactory
from tests.routers import CommonTestCase
from tests.utils import UserData, get_authorization_headers


class TestUser(CommonTestCase[User]):
    path = "/api/users/"
    services = UserServices()

    @override
    def assert_valid_response(self, response_data: dict) -> None:
        response_data = self.response_keys_to_snake_case(response_data)
        assert "id" in response_data, response_data
        assert "username" in response_data, response_data

    @override
    def assert_valid_response_values(self, response_data: dict, model: User) -> None:
        response_data = self.response_keys_to_snake_case(response_data)
        assert response_data["id"] == model.id, response_data
        assert response_data["username"] == model.username, response_data

    @override
    def build_model(self) -> User:
        return UserFactory.build()

    @override
    def create_model(self) -> User:
        return UserFactory.create()

    @override
    async def test_get_all(
        self,
        api_client: AsyncClient,
        authorization_headers: dict[str, str],
        model_count: int = 3,
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
            json=model.model_dump() | {"password": "<PASSWORD>"},
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
        self.assert_valid_response(response.json())

        assert (
            await self.services.get_by_id(response_data["id"], db_session) is not None
        )

    async def test_create_user_existing_username(
        self,
        api_client: AsyncClient,
        user_data: UserData,
    ):
        response = await api_client.post(self.path, json=user_data)  # type: ignore
        response_data = response.json()
        assert response.status_code == status.HTTP_400_BAD_REQUEST, response_data

    @override
    async def test_update(
        self,
        api_client: AsyncClient,
        *args,
        **kwargs,
    ):
        username = "user"
        password = "<PASSWORD>"
        user_data: UserData = {"username": username, "password": password}
        user = UserFactory.create(
            **user_data,
            hashed_password=get_password_hash(password),
        )
        authorization_headers = await get_authorization_headers(api_client, user_data)
        update_data = {"username": "new username"}

        # noinspection PyTestUnpassedFixture
        response = await api_client.patch(
            f"{self.path}{user.id}",
            json=update_data,
            headers=authorization_headers,
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK, response_data
        assert "username" in response_data, response_data
        assert response_data["username"] == update_data["username"], response_data

    async def test_update_other_user(
        self,
        api_client: AsyncClient,
        authorization_headers: dict[str, str],
    ):
        user = UserFactory.create()
        update_data = {"username": "new username"}

        response = await api_client.patch(
            f"{self.path}{user.id}",
            json=update_data,
            headers=authorization_headers,
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_403_FORBIDDEN, response_data

    async def test_update_other_user_as_admin(
        self,
        api_client: AsyncClient,
        admin_authorization_headers: dict[str, str],
    ):
        user = UserFactory.create()
        update_data = {"username": "new username"}

        response = await api_client.patch(
            f"{self.path}{user.id}",
            json=update_data,
            headers=admin_authorization_headers,
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK, response_data
        assert "username" in response_data, response_data
        assert response_data["username"] == update_data["username"], response_data

    async def test_update_non_existing_user(
        self,
        api_client: AsyncClient,
        authorization_headers: dict[str, str],
    ):
        response = await api_client.patch(
            f"{self.path}-1",
            json={"username": "new username"},
            headers=authorization_headers,
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_404_NOT_FOUND, response_data

    async def test_update_user_existing_name(
        self,
        api_client: AsyncClient,
        user_data: UserData,
    ):
        response = await api_client.post(self.path, json=user_data)  # type: ignore
        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text

    @override
    async def test_delete(
        self,
        api_client: AsyncClient,
        authorization_headers: dict[str, str],
        db_session: Session,
        *args,
        **kwargs,
    ):
        user = UserFactory.create()

        response = await api_client.delete(
            f"{self.path}{user.id}",
            headers=authorization_headers,
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN, response.json()

    async def test_delete_non_existing_user(
        self,
        api_client: AsyncClient,
        authorization_headers: dict[str, str],
    ):
        response = await api_client.delete(
            f"{self.path}-1", headers=authorization_headers
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN, response.json()

    async def test_delete_user_as_admin(
        self,
        api_client: AsyncClient,
        admin_authorization_headers: dict[str, str],
    ):
        user = UserFactory.create()

        response = await api_client.delete(
            f"{self.path}{user.id}",
            headers=admin_authorization_headers,
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT, response.text

    async def test_delete_non_existing_user_as_admin(
        self,
        api_client: AsyncClient,
        admin_authorization_headers: dict[str, str],
    ):
        response = await api_client.delete(
            f"{self.path}-1",
            headers=admin_authorization_headers,
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND, response.json()
