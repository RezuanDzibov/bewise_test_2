import pytest
from pytest_mock import MockerFixture

from core.settings import get_settings
from exceptions import AudioTrackFileNotFoundException
from services.audiotracks import construct_filepath_and_check_if_file_exists

settings = get_settings()


async def test_with_valid_filepath(mocker: MockerFixture, delete_all_media_after_tests: None):
    filename = "file.mp3"
    mocker.patch("os.path.isfile").return_value = True
    filepath = await construct_filepath_and_check_if_file_exists(path=filename)
    assert f"{settings.MEDIA_PATH}/{filename}" == filepath


async def test_with_invalid_filepath(mocker: MockerFixture, delete_all_media_after_tests: None):
    filename = "file.mp3"
    mocker.patch("os.path.isfile").return_value = False
    with pytest.raises(AudioTrackFileNotFoundException):
        await construct_filepath_and_check_if_file_exists(path=filename)
