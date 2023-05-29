from pydantic import BaseModel, constr, UUID4, conint


class UserInSchema(BaseModel):
    username: constr(min_length=5, max_length=250)


class UserOutSchema(BaseModel):
    id: conint(ge=1)
    access_token: UUID4
