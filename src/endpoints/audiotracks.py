import os

from fastapi import APIRouter, UploadFile, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import HttpUrl

from core.settings import get_settings
from dependencies import get_session
from schemas.audiotracks import AudioTrackInSchema, AudioFileInSchema
from services import audiotracks as audiotrack_services
from services.users import validate_user_access_token
from exceptions import AudioFileCorruptException, AudioTrackNotFoundException

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
        audiotrack_id = await audiotrack_services.insert_audiotrack_and_get_it_id(
            session, file=file, audiotrack_in_schema=audiotrack
        )
    except AudioFileCorruptException:
        raise HTTPException(status_code=400, detail="File corrupted")
    return f"{settings.API_URL}/audiotrack?id={audiotrack_id}&user={audiotrack.user_id}"


@router.get("")
async def get_audiotrack_file(
    audiotrack_in: AudioFileInSchema = Depends(),
    session: AsyncSession = Depends(get_session),
) -> FileResponse:
    try:
        audiotrack = await audiotrack_services.get_audiotrack(
            session=session, audiotrack_id=audiotrack_in.id, user_id=audiotrack_in.user
        )
    except AudioTrackNotFoundException:
        raise HTTPException(status_code=404, detail="Audiotrack not found")
    filepath = f"{settings.MEDIA_PATH}/{audiotrack.filepath}"
    if not os.path.isfile(filepath):
        raise HTTPException(status_code=404, detail="Audiotrack file not found")
    return FileResponse(
        path=filepath,
        filename=f"{audiotrack.filename}.mp3",
    )
