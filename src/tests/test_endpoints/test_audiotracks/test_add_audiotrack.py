from httpx import AsyncClient


async def test_with_valid_data_and_file(
    auth_test_client_and_user: list,
    wav_file_in_bytes: bytes,
    delete_all_media_after_tests: None,
):
    auth_test_client, user = auth_test_client_and_user

    response = await auth_test_client.post(
        "/audiotrack",
        data={"user_id": user.id},
        files={"file": ("test_file.wav", wav_file_in_bytes, "audio/wav")},
    )

    assert response.status_code == 200


async def test_with_invalid_user_id(
    auth_test_client_and_user: list, wav_file_in_bytes: bytes
):
    auth_test_client_and_user, user = auth_test_client_and_user

    response = await auth_test_client_and_user.post(
        "/audiotrack",
        data={"user_id": 2000},
        files={"file": ("test_file.wav", wav_file_in_bytes, "audio/wav")},
    )

    assert response.status_code == 403


async def test_without_access_token(test_client: AsyncClient, wav_file_in_bytes: bytes):
    response = await test_client.post(
        "/audiotrack",
        data={"user_id": 1},
        files={"file": ("test_file.wav", wav_file_in_bytes, "audio/wav")},
    )

    assert response.status_code == 403


async def test_without_file(auth_test_client_and_user: AsyncClient):
    auth_test_client, user = auth_test_client_and_user

    response = await auth_test_client.post("/audiotrack", data={"user_id": user.id})

    assert response.status_code == 422


async def test_file_with_invalid_extension(
    auth_test_client_and_user: list, wav_file_in_bytes: bytes
):
    auth_test_client, user = auth_test_client_and_user

    response = await auth_test_client.post(
        "/audiotrack",
        data={"user_id": user.id},
        files={"file": ("test_file.mp3", wav_file_in_bytes, "audio/mpeg3")},
    )

    assert response.status_code == 400


async def test_corrupt_file(auth_test_client_and_user: list):
    auth_test_client, user = auth_test_client_and_user

    response = await auth_test_client.post(
        "/audiotrack",
        data={"user_id": user.id},
        files={"file": ("test_file", b"content", "audio/wav")},
    )

    assert response.status_code == 400
