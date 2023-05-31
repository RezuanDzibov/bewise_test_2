from typing import AsyncGenerator

from fastapi import Depends, Security, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import conint
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import SessionLocal
from core.settings import get_settings
from schemas.users import UserSchema
from services.users import get_user_by_id_and_access_token

settings = get_settings()
bearer = HTTPBearer()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


async def get_user(
    user_id: conint(ge=1),
    auth_creds: HTTPAuthorizationCredentials = Security(bearer),
    session: AsyncSession = Depends(get_session),
) -> UserSchema:
    user = await get_user_by_id_and_access_token(
        session=session,
        user_id=user_id,
        access_token=auth_creds.credentials,
    )
    if not user:
        raise HTTPException(status_code=403, detail="User id or access token invalid")
    return user
