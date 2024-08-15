from datetime import datetime

from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow(), onupdate=datetime.utcnow(), nullable=False)
