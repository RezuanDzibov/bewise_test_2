import os

from fastapi import APIRouter, UploadFile, Depends, Form
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import conint

from core.settings import get_settings
from dependencies import get_session, get_user
from schemas.audiotracks import AudioFileInSchema, AudioTrackOutSchema
from schemas.users import UserSchema
from services import audiotracks as audiotrack_services
from exceptions import AudioFileCorruptException, AudioTrackNotFoundException

settings = get_settings()
router = APIRouter()


@router.post("", response_model=AudioTrackOutSchema)
async def add_audiotrack(
    file: UploadFile,
    user_id: conint(ge=1) = Form(...),
    user: UserSchema = Depends(get_user),
    session: AsyncSession = Depends(get_session),
):
    if user_id != user.id:
        raise HTTPException(status_code=403, detail="User id or access_token invalid")
    if file.content_type not in ["audio/wav", "audio/wave"]:
        raise HTTPException(
            status_code=400,
            detail=f"File type of {file.content_type} is not supported, only wav",
        )
    try:
        audiotrack_id = await audiotrack_services.insert_audiotrack_and_get_it_id(
            session, file=file, user_id=user.id
        )
    except AudioFileCorruptException:
        raise HTTPException(status_code=400, detail="File corrupted")
    return AudioTrackOutSchema(audiotrack_url=f"{settings.API_URL}/audiotrack?id={audiotrack_id}&user={user.id}")


@router.get("", response_class=FileResponse)
async def get_audiotrack_file(
    audiotrack_in: AudioFileInSchema = Depends(),
    session: AsyncSession = Depends(get_session),
):
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
