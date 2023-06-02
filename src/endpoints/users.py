from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_session
from schemas.users import UserInSchema, UserOutSchema
from services.users import insert_user

router = APIRouter()


@router.post("", response_model=UserOutSchema)
async def add_user(user: UserInSchema, session: AsyncSession = Depends(get_session)):
    user = await insert_user(session=session, user_in_schema=user)
    return UserOutSchema(**user.dict())
