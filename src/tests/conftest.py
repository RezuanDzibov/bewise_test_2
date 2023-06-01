import asyncio
import os
import shutil
from asyncio import AbstractEventLoop
from typing import Generator, AsyncGenerator

import pytest
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from core.settings import get_settings
from models import Base

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
