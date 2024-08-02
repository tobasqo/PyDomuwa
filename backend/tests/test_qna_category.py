from typing import Any

from fastapi import status
from fastapi.testclient import TestClient

from domuwa.models.qna_category import QnACategoryChoices
from tests.factories import QnACategoryFactory


QNA_CATEGORY_PREFIX = "/api/qna-categories/"


def assert_valid_response(response_data: dict[str, Any]):
    assert "id" in response_data, response_data
    assert "name" in response_data, response_data
    assert response_data["name"] in QnACategoryChoices._value2member_map_, response_data


def test_create_qna_category(api_client: TestClient):
    response = api_client.post(
        QNA_CATEGORY_PREFIX,
        json={"name": QnACategoryChoices.NSFW},
    )
    assert response.status_code == status.HTTP_201_CREATED, response.text
    response_data = response.json()
    assert_valid_response(response_data)

    response = api_client.get(f'{QNA_CATEGORY_PREFIX}{response_data["id"]}')
    assert response.status_code == status.HTTP_200_OK, response.text
    assert_valid_response(response.json())


def test_create_qna_category_invalid_name(api_client: TestClient):
    response = api_client.post(QNA_CATEGORY_PREFIX, json={"name": "not from enum"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text


def test_get_qna_category_by_id(api_client: TestClient):
    qna_category = QnACategoryFactory.create()
    response = api_client.get(f"{QNA_CATEGORY_PREFIX}{qna_category.id}")
    assert response.status_code == status.HTTP_200_OK, response.text
    assert_valid_response(response.json())


def test_get_non_existing_qna_category(api_client: TestClient):
    response = api_client.get(f"{QNA_CATEGORY_PREFIX}999")
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text


def test_get_all_qna_categories(api_client: TestClient):
    QnACategoryFactory.create(name=QnACategoryChoices.SFW)
    QnACategoryFactory.create(name=QnACategoryChoices.NSFW)

    response = api_client.get(QNA_CATEGORY_PREFIX)
    assert response.status_code == status.HTTP_200_OK, response.text
    response_data = response.json()

    assert isinstance(response_data, list), response_data
    assert len(response_data) >= 2, response_data

    for qna_category in response_data:
        assert_valid_response(qna_category)


def test_update_qna_category(api_client: TestClient):
    qna_category = QnACategoryFactory.create()
    updated_qna_category_data = {"name": QnACategoryChoices.NSFW}

    response = api_client.patch(
        f"{QNA_CATEGORY_PREFIX}{qna_category.id}",
        json=updated_qna_category_data,
    )
    assert response.status_code == status.HTTP_200_OK, response.text
    assert_valid_response(response.json())

    response = api_client.get(f"{QNA_CATEGORY_PREFIX}{qna_category.id}")
    assert response.status_code == status.HTTP_200_OK, response.text

    response_data = response.json()
    assert_valid_response(response_data)
    assert response_data["name"] == updated_qna_category_data["name"], response_data


def test_update_non_existing_qna_category(api_client: TestClient):
    response = api_client.patch(
        f"{QNA_CATEGORY_PREFIX}999",
        json={"name": QnACategoryChoices.NSFW},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text


def test_update_qna_category_invalid_name(api_client: TestClient):
    qna_category = QnACategoryFactory.create()

    response = api_client.patch(
        f"{QNA_CATEGORY_PREFIX}{qna_category.id}",
        json={"name": "not from enum"},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text


def test_delete_qna_category(api_client: TestClient):
    qna_category = QnACategoryFactory.create()
    response = api_client.delete(f"{QNA_CATEGORY_PREFIX}{qna_category.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.text

    response = api_client.get(f"{QNA_CATEGORY_PREFIX}{qna_category.id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text


def test_delete_non_existing_qna_category(api_client: TestClient):
    response = api_client.delete(f"{QNA_CATEGORY_PREFIX}999")
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
