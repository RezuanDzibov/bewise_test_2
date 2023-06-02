from httpx import AsyncClient

from schemas.users import UserSchema


async def test_with_valid_data(test_client: AsyncClient, built_user: UserSchema):
    response = await test_client.post("/user", json={"username": built_user.username})
    assert response.status_code == 200



async def test_with_not_exists_fields(test_client: AsyncClient, built_user: UserSchema):
    response = await test_client.post("/user", json={"username": built_user.username, "age": 27})
    assert response.status_code == 200


async def test_with_invalid_data(test_client: AsyncClient):
    response = await test_client.post("/user", json={"username": 2000})
    assert response.status_code == 422


