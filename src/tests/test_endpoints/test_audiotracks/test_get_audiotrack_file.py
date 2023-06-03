from uuid import uuid4

from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from schemas.audiotracks import AudioTrackSchema


async def test_exists_audiotrack_and_file(
    auth_test_client_and_user: list[AsyncClient, User],
    added_audiotrack: dict[str, str],
    delete_all_media_after_tests: None,
):
    auth_test_client, user = auth_test_client_and_user

    response = await auth_test_client.get(
        f"/audiotrack?id={added_audiotrack['id']}&user={added_audiotrack['user']}"
    )

    assert response.status_code == 200


async def test_not_exists_audiotrack(
    auth_test_client_and_user: list[AsyncClient, User]
):
    auth_test_client, user = auth_test_client_and_user

    response = await auth_test_client.get(f"/audiotrack?id={uuid4()}&user={user.id}")

    assert response.status_code == 404


async def test_not_exists_file(
    session: AsyncSession, test_client: AsyncClient, audiotrack: AudioTrackSchema
):
    statement = select(User).where(User.id == audiotrack.author)
    result = await session.execute(statement)
    user = result.scalar()
    test_client.headers["Authorization"] = f"bearer {user.access_token}"

    response = await test_client.get(f"/audiotrack?id={audiotrack.id}&user={user.id}")

    assert response.status_code == 404
