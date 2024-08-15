from typing import Optional, Union

import uuid
import datetime

from sqlalchemy import DATE, TEXT, ForeignKey, FLOAT, BOOLEAN, UniqueConstraint, UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects import postgresql as pg

from .base import Base
from .enums import DataType


DataReturnType = Union[str, float, datetime.date, bool, dict]


class DataStore(Base):
    __tablename__ = 'data_store'
    __table_args__ = (
        UniqueConstraint('event_id', 'tag_id'),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    event_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID, ForeignKey('event.id'))
    tag_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey('tag.id'))

    # Data Options
    text: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)
    number: Mapped[Optional[float]] = mapped_column(FLOAT, nullable=True)
    date: Mapped[Optional[datetime.date]] = mapped_column(DATE, nullable=True)
    boolean: Mapped[Optional[bool]] = mapped_column(BOOLEAN, nullable=True)
    complex: Mapped[Optional[dict]] = mapped_column(pg.JSON, nullable=True)

    def value(self, expected_data_type: DataType) -> Optional[DataReturnType]:
        if expected_data_type == DataType.number:
            return self.number
        
        if expected_data_type == DataType.text:
            return self.text
        
        if expected_data_type == DataType.date:
            return self.date
        
        if expected_data_type == DataType.boolean:
            return self.boolean
        
        if expected_data_type == DataType.complex:
            return self.complex
        
        return None
