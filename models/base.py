from typing import TypeVar

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.types import Integer


class Base(DeclarativeBase):
    id: Integer
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


BaseModel = TypeVar("BaseModel", bound=Base)
