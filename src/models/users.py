from uuid import uuid4

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from models import Base


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    access_token: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid4)
