from fastapi import APIRouter

from endpoints.audiotracks import router as audiotrack_router
from endpoints.users import router as user_router

router = APIRouter()

router.include_router(user_router, prefix="/user", tags=["user"])
router.include_router(audiotrack_router, prefix="/audiotrack", tags=["audiotrack"])
