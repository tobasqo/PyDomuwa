from typing import TypedDict

from httpx import AsyncClient


class UserData(TypedDict):
    username: str
    password: str


def get_default_user_data() -> UserData:
    return UserData(
        username="user",
        password="<PASSWORD>",
    )


async def get_authorization_headers(api_client: AsyncClient, user_data: UserData):
    response = await api_client.post("/auth/token", data=user_data)  # type: ignore
    response_data = response.json()
    access_token = response_data["accessToken"]
    return {"Authorization": f"Bearer {access_token}"}
