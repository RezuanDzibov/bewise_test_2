from pydantic import BaseModel, conint, UUID4


class AudioTrackInSchema(BaseModel):
    user_id: conint(ge=1)
    access_token: UUID4


class AudioFileInSchema(BaseModel):
    id: UUID4
    user: conint(ge=1)
