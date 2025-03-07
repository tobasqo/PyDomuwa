from typing import NotRequired, TypedDict

from httpx import AsyncClient


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


async def get_authorization_headers(api_client: AsyncClient, user_data: UserData):
    response = await api_client.post("/auth/token", data=user_data)  # type: ignore
    response_data = response.json()
    access_token = response_data["accessToken"]
    return {"Authorization": f"Bearer {access_token}"}
