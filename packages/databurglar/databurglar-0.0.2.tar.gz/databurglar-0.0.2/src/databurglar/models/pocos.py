from dataclasses import dataclass
from typing import Optional

from .typings import DataReturnType


@dataclass
class Measurement:
    value: Optional[DataReturnType]
    units: str
