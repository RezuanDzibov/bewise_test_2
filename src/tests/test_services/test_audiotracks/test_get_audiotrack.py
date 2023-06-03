import random
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions import AudioTrackNotFoundException
from schemas.audiotracks import AudioTrackSchema
from services.audiotracks import get_audiotrack


async def test_audiotrack_exists(audiotrack: AudioTrackSchema, session: AsyncSession):
    audiotrack_in_db = await get_audiotrack(
        session=session, audiotrack_id=audiotrack.id, user_id=audiotrack.author
    )
    assert audiotrack == audiotrack_in_db


async def test_audiotrack_not_exists(session: AsyncSession):
    with pytest.raises(AudioTrackNotFoundException):
        await get_audiotrack(session=session, audiotrack_id=uuid4(), user_id=2)


async def test_many_audiotrack_exist(
    audiotracks: list[AudioTrackSchema], session: AsyncSession
):
    audiotrack = random.choice(audiotracks)
    audiotrack_in_db = await get_audiotrack(
        session=session, audiotrack_id=audiotrack.id, user_id=audiotrack.author
    )
    assert audiotrack == audiotrack_in_db
