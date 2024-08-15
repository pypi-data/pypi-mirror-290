from typing import Optional

import uuid

from sqlalchemy import Enum, String, UniqueConstraint, UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .base import Base
from .enums import DataType


class Tag(Base):
    __tablename__ = 'tag'
    __table_args__ = (
        UniqueConstraint('code'),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    data_type: Mapped[DataType] = mapped_column(Enum(DataType), nullable=False)
    code: Mapped[str] = mapped_column(String(10))
    name: Mapped[Optional[str]] = mapped_column(String(125), nullable=True)
