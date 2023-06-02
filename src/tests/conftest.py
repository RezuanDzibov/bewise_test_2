import asyncio
import os
import shutil
from asyncio import AbstractEventLoop
from io import BytesIO
from typing import Generator, AsyncGenerator

import aiofiles
import pytest
from faker import Faker
from fastapi import UploadFile
from pytest_asyncio.plugin import SubRequest
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from starlette.datastructures import Headers

from tests import factories
from core.settings import get_settings, BASE_DIR
from models import Base, User
from schemas.audiotracks import AudioTrackSchema

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
    audiotrack = factories.AudioTrackFactory(author=user.id, filename="filename.mp3", filepath="filename.mp3")
    session.add(audiotrack)
    await session.commit()
    return AudioTrackSchema.from_orm(audiotrack)


@pytest.fixture(scope="function")
async def audiotracks(request: SubRequest, session: AsyncSession, user: User) -> list[AudioTrackSchema]:
    if (
        hasattr(request, "param")
        and isinstance(request.param, int)
        and request.param > 0
    ):
        audiotrack_num = request.param
    else:
        audiotrack_num = 1
    audiotracks = factories.AudioTrackFactory.build_batch(
        audiotrack_num,
        filename="filename.mp3",
        filepath="filename.mp3",
        author=user.id
    )
    session.add_all(audiotracks)
    await session.commit()
    return [AudioTrackSchema.from_orm(audiotrack) for audiotrack in audiotracks]


@pytest.fixture(scope="function")
async def upload_file() -> UploadFile:
    async with aiofiles.open(f"{BASE_DIR}/src/tests/test_file.wav", "rb") as buffer:
        file = UploadFile(
            file=BytesIO(await buffer.read()),
            filename="test_file.wav",
            headers=Headers({"content-type": "audio/wav"})
        )
        return file


@pytest.fixture(scope="function")
async def invalid_upload_file() -> UploadFile:
    bytes_content = bytearray(b"somecontent")
    file = UploadFile(
        file=BytesIO(bytes_content),
        filename="test_file.wav",
        headers=Headers({"content-type": "audio/wav"})
    )
    return file


@pytest.fixture(scope="function")
async def mp3_upload_file() -> UploadFile:
    async with aiofiles.open(f"{BASE_DIR}/src/tests/test_file.mp3", "rb") as buffer:
        file = UploadFile(
            file=BytesIO(await buffer.read()),
            filename="test_file.mp3",
            headers=Headers({"content-type": "audio/wav"})
        )
        return file


@pytest.fixture(scope="function")
async def built_user() -> User:
    return factories.UserFactory.build()
