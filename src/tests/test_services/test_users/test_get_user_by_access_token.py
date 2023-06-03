import random
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from schemas.users import UserSchema
from services.users import get_user_by_access_token


async def test_user_exists(user: User, session: AsyncSession):
    user_in_db = await get_user_by_access_token(
        session=session, access_token=str(user.access_token)
    )
    assert UserSchema.from_orm(user) == user_in_db


async def test_many_user_exist(users: list[UserSchema], session: AsyncSession):
    user = random.choice(users)
    user_in_db = await get_user_by_access_token(
        session=session, access_token=user.access_token
    )
    assert user == user_in_db


async def test_user_not_exists(session: AsyncSession):
    user = await get_user_by_access_token(session=session, access_token=str(uuid4()))
    assert not user
