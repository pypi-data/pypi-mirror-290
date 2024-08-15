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
    name: Mapped[str] = mapped_column(String(125))
    units: Mapped[str] = mapped_column(String(15), nullable=True)

    @property
    def is_measurement(self) -> bool:
        return self.units not in ('', None)
