from pydantic import BaseModel


class Attachment(BaseModel):
    key: str
    type: str
    data: str
