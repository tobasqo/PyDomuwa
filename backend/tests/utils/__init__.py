from typing import NotRequired, TypedDict

from starlette.testclient import TestClient


class UserData(TypedDict):
    username: str
    password: str
    is_active: NotRequired[bool]
    is_staff: NotRequired[bool]


def get_default_user_data() -> UserData:
    return UserData(
        username="user",
        password="<PASSWORD>",
        is_active=True,
        is_staff=False,
    )


def get_authorization_headers(api_client: TestClient, user_data: UserData):
    response = api_client.post("/auth/login", data=user_data)  # type: ignore
    response_data = response.json()
    access_token = response_data["access_token"]
    return {"Authorization": f"Bearer {access_token}"}
