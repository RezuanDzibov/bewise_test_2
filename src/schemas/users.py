from pydantic import BaseModel, constr, UUID4, conint


class UserInSchema(BaseModel):
    username: constr(min_length=5, max_length=250)


class UserOutSchema(BaseModel):
    id: conint(ge=1)
    access_token: UUID4


class UserSchema(BaseModel):
    id: conint(ge=1)
    username: str
    access_token: UUID4

    class Config:
        orm_mode = True
