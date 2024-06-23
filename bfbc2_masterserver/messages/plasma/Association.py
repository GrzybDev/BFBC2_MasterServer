from datetime import datetime

from pydantic import BaseModel


class Association(BaseModel):
    id: int
    name: str
    type: int
    created: datetime
    modified: datetime
