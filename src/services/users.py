from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from schemas.users import UserInSchema, UserOutSchema


async def insert_user(
    session: AsyncSession, user_in_schema: UserInSchema
) -> UserOutSchema:
    statement = insert(User).values(user_in_schema.dict())
    statement = statement.returning(User)
    result = await session.execute(statement)
    await session.commit()
    user_in_db = result.scalar()
    user_out_schema = UserOutSchema(
        id=user_in_db.id, access_token=user_in_db.access_token
    )
    return user_out_schema
