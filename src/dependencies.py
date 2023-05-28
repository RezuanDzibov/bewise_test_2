from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from core.db import SessionLocal
from core.settings import get_settings

settings = get_settings()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
