from pydantic import BaseModel, constr, UUID4


class UserInSchema(BaseModel):
    username: constr(min_length=5, max_length=250)


class UserOutSchema(BaseModel):
    id: int
    access_token: UUID4
