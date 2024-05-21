from pydantic import BaseModel


class PlasmaChunk(BaseModel):
    data: str
    decodedSize: int
    size: int
