from pydantic import BaseModel


class Stat(BaseModel):
    key: str
    value: float
