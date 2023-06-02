from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from schemas.users import UserInSchema, UserSchema


async def insert_user(
    session: AsyncSession, user_in_schema: UserInSchema
) -> UserSchema:
    statement = insert(User).values(user_in_schema.dict())
    statement = statement.returning(User)
    result = await session.execute(statement)
    await session.commit()
    user_in_db = result.scalar()
    user_schema = UserSchema.from_orm(user_in_db)
    return user_schema


async def get_user_by_access_token(
    session: AsyncSession, access_token: str
) -> UserSchema | None:
    statement = select(User).where(User.access_token == access_token)
    result = await session.execute(statement)
    user = result.scalar()
    return UserSchema.from_orm(user) if user else None
