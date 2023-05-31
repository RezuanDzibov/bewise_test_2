import asyncio
import concurrent.futures
import io
import os.path
from datetime import datetime
from uuid import UUID

import aiofiles
from fastapi import UploadFile
from pydub import AudioSegment
from pydub.exceptions import PydubException
from sqlalchemy import insert, select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from core.settings import get_settings
from exceptions import AudioFileCorruptException, AudioTrackNotFoundException, AudioTrackFileNotFoundException
from models.audiotracks import AudioTrack

settings = get_settings()


async def _generate_filepath(filename: str, user_id: int) -> str:
    current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
    return str(settings.MEDIA_PATH / f"{current_datetime}_{user_id}_{filename}")


async def _insert_audiotrack(
    session: AsyncSession, user_id: int, filepath: str, filename: str
) -> UUID:
    statement = insert(AudioTrack).values(
        author=user_id, filepath=filepath, filename=filename
    )
    statement = statement.returning(AudioTrack.id)
    result = await session.execute(statement)
    await session.commit()
    return result.scalar()


async def _save_file(filepath: str, file_content: bytes) -> None:
    async with aiofiles.open(filepath, mode="wb") as buffer:
        await buffer.write(file_content)


def _convert_wav_to_mp3(file_content: bytes) -> bytes:
    try:
        wav_file = AudioSegment.from_wav(io.BytesIO(file_content))
    except PydubException:
        raise AudioFileCorruptException
    mp3_file = io.BytesIO()
    try:
        wav_file.export(mp3_file, format="mp3")
    except PydubException:
        raise AudioFileCorruptException
    mp3_file.seek(0)
    return mp3_file.read()


async def insert_audiotrack_and_get_it_id(
    session: AsyncSession, file: UploadFile, user_id: int
) -> UUID:
    file_content = await file.read()
    loop = asyncio.get_event_loop()
    with concurrent.futures.ProcessPoolExecutor() as pool:
        file_content_in_mp3 = await loop.run_in_executor(
            pool, _convert_wav_to_mp3, file_content
        )
    filepath = await _generate_filepath(
        filename=file.filename.split(".")[0] + ".mp3",
        user_id=user_id,
    )
    await _save_file(filepath=filepath, file_content=file_content_in_mp3)
    return await _insert_audiotrack(
        session,
        user_id=user_id,
        filepath=filepath.split("/")[-1],
        filename=file.filename.split(".")[0],
    )


async def construct_filepath_and_check_if_file_exists(path: str):
    filepath = f"{settings.MEDIA_PATH}/{path}"
    if not os.path.isfile(filepath):
        raise AudioTrackFileNotFoundException
    return filepath


async def get_audiotrack(session: AsyncSession, audiotrack_id: UUID, user_id: int):
    statement = select(AudioTrack).where(
        and_(AudioTrack.id == audiotrack_id, AudioTrack.author == user_id)
    )
    result = await session.execute(statement)
    audiotrack = result.scalar()
    if not audiotrack:
        raise AudioTrackNotFoundException
    return audiotrack
