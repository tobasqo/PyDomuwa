from fastapi import status
from httpx import AsyncClient
from sqlmodel import Session
from typing_extensions import override

from domuwa.models.qna_category import QnACategory, QnACategoryChoices
from domuwa.services.qna_categories_services import QnACategoryServices
from tests.factories import QnACategoryFactory
from tests.routers import CommonTestCase


class TestQnACategory(CommonTestCase[QnACategory]):
    path = "/api/qna-categories/"
    services = QnACategoryServices()

    @override
    def assert_valid_response(self, response_data: dict) -> None:
        assert "id" in response_data, response_data
        assert "name" in response_data, response_data
        assert (
            response_data["name"] in QnACategoryChoices._value2member_map_
        ), response_data

    @override
    def assert_valid_response_values(
        self,
        response_data: dict,
        model: QnACategory,
    ) -> None:
        assert response_data["id"] == model.id
        assert response_data["name"] == model.name

    @override
    def build_model(self) -> QnACategory:
        return QnACategoryFactory.build()

    @override
    def create_model(self) -> QnACategory:
        return QnACategoryFactory.create()

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
        qna_category: QnACategory = QnACategoryFactory.create(
            name=QnACategoryChoices.SFW
        )

        response = await api_client.post(
            self.path,
            json={"name": qna_category.name},
            headers=admin_authorization_headers,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text

    @override
    async def test_update(  # type: ignore
        self,
        api_client: AsyncClient,
        admin_authorization_headers: dict[str, str],
        *args,
        **kwargs,
    ):
        qna_category: QnACategory = QnACategoryFactory.create()
        updated_qna_category_data = {"name": QnACategoryChoices.NSFW}

        response = await api_client.patch(
            f"{self.path}{qna_category.id}",
            json=updated_qna_category_data,
            headers=admin_authorization_headers,
        )
        assert response.status_code == status.HTTP_200_OK, response.text
        self.assert_valid_response(response.json())

        response = await api_client.get(
            f"{self.path}{qna_category.id}",
            headers=admin_authorization_headers,
        )
        assert response.status_code == status.HTTP_200_OK, response.text

        response_data = response.json()
        self.assert_valid_response(response_data)
        assert response_data["name"] == updated_qna_category_data["name"], response_data

    async def test_update_non_admin(
        self,
        api_client: AsyncClient,
        authorization_headers: dict[str, str],
    ):
        qna_category: QnACategory = QnACategoryFactory.create()
        updated_qna_category_data = {"name": QnACategoryChoices.NSFW}

        response = await api_client.patch(
            f"{self.path}{qna_category.id}",
            json=updated_qna_category_data,
            headers=authorization_headers,
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN, response.text

    async def test_update_invalid_name(
        self,
        api_client: AsyncClient,
        admin_authorization_headers: dict[str, str],
    ):
        qna_category: QnACategory = QnACategoryFactory.create()

        response = await api_client.patch(
            f"{self.path}{qna_category.id}",
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
        qna_category1: QnACategory = QnACategoryFactory.create(
            name=QnACategoryChoices.SFW
        )
        qna_category2: QnACategory = QnACategoryFactory.create(
            name=QnACategoryChoices.NSFW
        )

        response = await api_client.patch(
            f"{self.path}{qna_category1.id}",
            json={"name": qna_category2.name},
            headers=admin_authorization_headers,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text

    @override
    async def test_get_all(  # type: ignore
        self,
        api_client: AsyncClient,
        authorization_headers: dict[str, str],
        model_count: int = 2,
        *args,
        **kwargs,
    ):
        QnACategoryFactory.create(name=QnACategoryChoices.SFW)
        QnACategoryFactory.create(name=QnACategoryChoices.NSFW)

        response = await api_client.get(self.path, headers=authorization_headers)
        assert response.status_code == status.HTTP_200_OK, response.text
        response_data = response.json()

        assert isinstance(response_data, list), response_data
        assert len(response_data) >= 2, response_data

        for qna_category in response_data:
            self.assert_valid_response(qna_category)

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
