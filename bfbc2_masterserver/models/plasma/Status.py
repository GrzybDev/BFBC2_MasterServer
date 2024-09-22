from pydantic import BaseModel


class Status(BaseModel):
    userid: int
    status: int
