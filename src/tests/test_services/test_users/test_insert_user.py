from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from schemas.users import UserInSchema
from services.users import insert_user


async def test_with_valid_data(session: AsyncSession, built_user: User):
    built_user_schema = UserInSchema(username=built_user.username)
    user = await insert_user(session=session, user_in_schema=built_user_schema)
    assert built_user_schema.username == user.username
