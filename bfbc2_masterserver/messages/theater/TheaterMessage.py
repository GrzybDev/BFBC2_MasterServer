from typing import Optional

from pydantic import BaseModel


class TheaterMessage(BaseModel):
    TID: Optional[int] = None
