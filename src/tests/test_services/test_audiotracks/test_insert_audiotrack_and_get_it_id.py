import pytest
from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions import AudioFileCorruptException
from models import User, AudioTrack
from services.audiotracks import insert_audiotrack_and_get_it_id, get_filename_with_mp3_extension


async def test_with_valid_file_and_data(
        delete_all_media_after_tests: None,
        user: User,
        session: AsyncSession,
        wav_upload_file: UploadFile
):
    audiotrack_id = await insert_audiotrack_and_get_it_id(session=session, file=wav_upload_file, user_id=user.id)
    statement = select(AudioTrack).where(AudioTrack.id == audiotrack_id)
    result = await session.execute(statement)
    audiotrack_in_db = result.scalar()
    assert audiotrack_id == audiotrack_in_db.id
    assert await get_filename_with_mp3_extension(wav_upload_file.filename) == audiotrack_in_db.filename


async def test_with_corrupt_file(
        delete_all_media_after_tests: None,
        user: User,
        session: AsyncSession,
        invalid_upload_file: UploadFile
):
    with pytest.raises(AudioFileCorruptException):
        await insert_audiotrack_and_get_it_id(session=session, file=invalid_upload_file, user_id=user.id)


async def test_file_with_mp3_extension(
        delete_all_media_after_tests: None,
        user: User,
        session: AsyncSession,
        mp3_upload_file: UploadFile
):
    with pytest.raises(AudioFileCorruptException):
        await insert_audiotrack_and_get_it_id(session=session, file=mp3_upload_file, user_id=user.id)
