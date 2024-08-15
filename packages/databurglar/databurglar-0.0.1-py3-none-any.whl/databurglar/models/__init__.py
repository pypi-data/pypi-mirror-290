from typing import cast
from sqlalchemy import Engine, Table

from .base import Base
from .enums import DataType
from .events import UserEvent
from .tag import Tag
from .data_store import DataStore
from .survey import Survey
from .survey_question import SurveyQuestion


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
