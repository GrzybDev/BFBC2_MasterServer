from typing import Optional

from pydantic import BaseModel


class TheaterTransaction(BaseModel):
    TID: Optional[int] = None
