import uuid

from datetime import datetime
from sqlalchemy import UUID, String, TIMESTAMP, UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .base import Base


class UserEvent(Base):
    __tablename__ = 'event'
    __table_args__ = (
        UniqueConstraint('user_id', 'label', 'timestamp'),
    )
    __description__ = 'User did "something" at "some specific time"'

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False)
    label: Mapped[str] = mapped_column(String(125))
    timestamp: Mapped[datetime] = mapped_column(TIMESTAMP)
