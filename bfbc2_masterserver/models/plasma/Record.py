from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Record(BaseModel):
    key: int
    value: str
    updated: Optional[datetime] = None
