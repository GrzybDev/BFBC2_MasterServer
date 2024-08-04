from pydantic import BaseModel


class Partition(BaseModel):
    partition: str
