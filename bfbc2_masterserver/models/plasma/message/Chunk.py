from typing import Optional

from pydantic import BaseModel


class Chunk(BaseModel):
    data: str
    decodedSize: Optional[int] = None
    size: int
