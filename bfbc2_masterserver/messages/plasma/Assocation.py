from datetime import datetime

from pydantic import BaseModel


class Assocation(BaseModel):
    id: int
    name: str
    type: int
    created: datetime
    modified: datetime
