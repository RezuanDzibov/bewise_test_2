from uuid import uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from models import Base


class AudioTrack(Base):
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), default=uuid4, primary_key=True, index=True
    )
    file_path: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[int] = mapped_column(ForeignKey("user.id"))
