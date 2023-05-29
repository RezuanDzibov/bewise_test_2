from fastapi import APIRouter, UploadFile, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import HttpUrl

from core.settings import get_settings
from dependencies import get_session
from schemas.audiotracks import AudioTrackInSchema
from services.audiotracks import insert_audiotrack_and_get_it_id
from services.users import validate_user_access_token
from exceptions import AudioFileCorruptException

settings = get_settings()
router = APIRouter()


@router.post("", response_model=HttpUrl)
async def add_audiotrack(
    file: UploadFile,
    audiotrack: AudioTrackInSchema = Depends(),
    session: AsyncSession = Depends(get_session),
):
    if file.content_type != "audio/wav":
        raise HTTPException(
            status_code=400,
            detail=f"File type of {file.content_type} is not supported, only wav",
        )
    if not await validate_user_access_token(
        session=session,
        user_id=audiotrack.user_id,
        access_token=audiotrack.access_token,
    ):
        raise HTTPException(status_code=403, detail="User id or access token invalid")
    try:
        audiotrack_id = await insert_audiotrack_and_get_it_id(
            session, file=file, audiotrack_in_schema=audiotrack
        )
    except AudioFileCorruptException:
        raise HTTPException(status_code=400, detail="File corrupted")
    return f"http://{settings.API_HOST}:{settings.API_PORT}/audiotracks?id={audiotrack_id}&user={audiotrack.user_id}"
