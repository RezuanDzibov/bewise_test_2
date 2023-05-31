from sqlalchemy import insert, select

from models import User
from schemas.users import UserInSchema, UserOutSchema, UserSchema


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


async def get_user_by_access_token(
    session: AsyncSession, access_token: str
) -> UserSchema | None:
    statement = select(User).where(User.access_token == access_token)
    result = await session.execute(statement)
    user = result.scalar()
    return UserSchema.from_orm(user) if user else None
