from services.audiotracks import get_filename_with_mp3_extension


async def test_with_valid_filename():
    filename = "filename"
    filename_with_mp3_extension = await get_filename_with_mp3_extension(filename=f"{filename}.wav")
    assert f"{filename}.mp3" == filename_with_mp3_extension


async def test_filename_with_two_extensions():
    filename = "filename.mp3"
    filename_with_mp3_extension = await get_filename_with_mp3_extension(filename=f"{filename}.wav")
    assert f"{filename}.mp3" == filename_with_mp3_extension
