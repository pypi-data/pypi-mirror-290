from typing import List

import uuid

from sqlalchemy import TEXT, ForeignKey, String, UniqueConstraint, UUID, BOOLEAN
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects import postgresql as pg

from .base import Base


class SurveyQuestion(Base):
    __tablename__ = 'survey_question'
    __table_args__ = (
        UniqueConstraint('survey_id', 'tag_id'),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    survey_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey('survey.id'))
    tag_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey('tag.id'))

    text: Mapped[str] = mapped_column(TEXT)

    is_required: Mapped[bool] = mapped_column(BOOLEAN, default=False)
    validators: Mapped[List[str]] = mapped_column(
        pg.ARRAY(String(125)),
        default=list
    )
