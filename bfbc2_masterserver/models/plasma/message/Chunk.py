from pydantic import BaseModel


class Chunk(BaseModel):
    data: str
    decodedSize: int
    size: int
