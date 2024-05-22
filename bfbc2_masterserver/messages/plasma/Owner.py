from typing import Optional

from pydantic import BaseModel


class Owner(BaseModel):
    id: int
    name: Optional[str] = None
    type: int
