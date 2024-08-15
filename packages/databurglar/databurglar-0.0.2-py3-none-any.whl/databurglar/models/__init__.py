from typing import cast
from sqlalchemy import Engine, Table

from .base import Base
from .typings import DataReturnType
from .pocos import Measurement
from .enums import DataType
from .events import UserEvent
from .tag import Tag
from .survey_question import SurveyQuestion
from .data_store import DataStore, TaggedData
from .survey import Survey


def setup_data_collection(engine: Engine, event_table: Base):
    Base.metadata.create_all(engine, tables=[
        cast(Table, event_table.__table__),
        cast(Table, Tag.__table__),
        cast(Table, DataStore.__table__),
    ])

def setup_surveys(engine: Engine):
    Base.metadata.create_all(engine, tables=[
        cast(Table, Survey.__table__),
        cast(Table, SurveyQuestion.__table__)
    ])
