from typing import AsyncGenerator

from fastapi import Depends, Security, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import conint


from core.db import SessionLocal
from core.settings import get_settings
from schemas.users import UserSchema
from services.users import get_user_by_access_token


settings = get_settings()
bearer = HTTPBearer()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


async def get_user(
    auth_creds: HTTPAuthorizationCredentials = Security(bearer),
    session: AsyncSession = Depends(get_session),
) -> UserSchema:
    user = await get_user_by_access_token(
        session=session,
        access_token=auth_creds.credentials,
    )
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user
