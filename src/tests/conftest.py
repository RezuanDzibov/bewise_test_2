import asyncio
import json
import os
import shutil
from asyncio import AbstractEventLoop
from io import BytesIO
from typing import Generator, AsyncGenerator
from urllib.parse import urlparse, parse_qs

import aiofiles
import pytest
from faker import Faker
from fastapi import UploadFile
from httpx import AsyncClient
from pytest_asyncio.plugin import SubRequest
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from starlette.datastructures import Headers

from core.settings import get_settings, BASE_DIR
from main import app
from models import Base, User
from schemas.audiotracks import AudioTrackSchema
from schemas.users import UserSchema
from tests import factories

settings = get_settings()
fake = Faker()


@pytest.fixture(scope="session")
def event_loop() -> Generator[AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def engine() -> AsyncEngine:
    return create_async_engine(settings.SQLALCHEMY_DATABASE_URI)


@pytest.fixture(scope="function")
async def init_tables(engine: AsyncEngine) -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
    await engine.dispose()


@pytest.fixture(scope="function")
async def session_maker(engine: AsyncEngine) -> sessionmaker:
    return sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )


@pytest.fixture(scope="function")
async def session(
    init_tables: None, session_maker: session_maker
) -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session


@pytest.fixture(scope="function")
async def delete_all_media_after_tests() -> AsyncGenerator[None, None]:
    if not os.path.isdir(settings.MEDIA_PATH):
        os.makedirs(settings.MEDIA_PATH)
    yield
    shutil.rmtree(settings.MEDIA_PATH)
    os.makedirs(settings.MEDIA_PATH)


@pytest.fixture(scope="function")
async def user(session: AsyncSession) -> User:
    user = factories.UserFactory()
    session.add(user)
    await session.commit()
    return user


@pytest.fixture(scope="function")
async def audiotrack(session: AsyncSession, user: User) -> AudioTrackSchema:
    audiotrack = factories.AudioTrackFactory(
        author=user.id, filename="filename.mp3", filepath="filename.mp3"
    )
    session.add(audiotrack)
    await session.commit()
    return AudioTrackSchema.from_orm(audiotrack)


@pytest.fixture(scope="function")
async def audiotracks(
    request: SubRequest, session: AsyncSession, user: User
) -> list[AudioTrackSchema]:
    if (
        hasattr(request, "param")
        and isinstance(request.param, int)
        and request.param > 0
    ):
        audiotrack_num = request.param
    else:
        audiotrack_num = 1
    audiotracks = factories.AudioTrackFactory.build_batch(
        audiotrack_num, filename="filename.mp3", filepath="filename.mp3", author=user.id
    )
    session.add_all(audiotracks)
    await session.commit()
    return [AudioTrackSchema.from_orm(audiotrack) for audiotrack in audiotracks]


@pytest.fixture(scope="function")
async def wav_upload_file() -> UploadFile:
    async with aiofiles.open(f"{BASE_DIR}/src/tests/test_file.wav", "rb") as buffer:
        file = UploadFile(
            file=BytesIO(await buffer.read()),
            filename="test_file.wav",
            headers=Headers({"content-type": "audio/wav"}),
        )
        return file


@pytest.fixture(scope="function")
async def invalid_upload_file() -> UploadFile:
    bytes_content = bytearray(b"somecontent")
    file = UploadFile(
        file=BytesIO(bytes_content),
        filename="test_file.wav",
        headers=Headers({"content-type": "audio/wav"}),
    )
    return file


@pytest.fixture(scope="function")
async def mp3_upload_file() -> UploadFile:
    async with aiofiles.open(f"{BASE_DIR}/src/tests/test_file.mp3", "rb") as buffer:
        file = UploadFile(
            file=BytesIO(await buffer.read()),
            filename="test_file.mp3",
            headers=Headers({"content-type": "audio/wav"}),
        )
        return file


@pytest.fixture(scope="function")
async def built_user() -> User:
    return factories.UserFactory.build()


@pytest.fixture(scope="function")
async def users(request: SubRequest, session: AsyncSession) -> list[UserSchema]:
    if (
        hasattr(request, "param")
        and isinstance(request.param, int)
        and request.param > 0
    ):
        user_num = request.param
    else:
        user_num = 1
    users = factories.UserFactory.build_batch(user_num)
    session.add_all(users)
    await session.commit()
    return [UserSchema.from_orm(user) for user in users]


@pytest.fixture(scope="function")
async def test_client() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client


@pytest.fixture(scope="function")
async def auth_test_client_and_user(
    test_client: AsyncClient, user: User
) -> AsyncClient:
    test_client.headers["Authorization"] = f"bearer {user.access_token}"
    yield test_client, user


@pytest.fixture(scope="function")
async def wav_file_in_bytes() -> bytes:
    async with aiofiles.open(f"{BASE_DIR}/src/tests/test_file.wav", "rb") as buffer:
        yield await buffer.read()


@pytest.fixture(scope="function")
async def added_audiotrack(
    auth_test_client_and_user: list, wav_file_in_bytes: bytes
) -> dict[str, str]:
    auth_test_client, user = auth_test_client_and_user
    response = await auth_test_client.post(
        "/audiotrack",
        data={"user_id": user.id},
        files={"file": ("test_file.wav", wav_file_in_bytes, "audio/wav")},
    )
    response_content = json.loads(response.content.decode("utf-8"))
    parsed_url = urlparse(response_content["audiotrack_url"])
    return {key: value[0] for key, value in parse_qs(parsed_url.query).items()}
