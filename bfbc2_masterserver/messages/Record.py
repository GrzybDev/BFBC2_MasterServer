from datetime import datetime

from pydantic import BaseModel


class Record(BaseModel):
    key: int
    value: str
    updated: datetime
