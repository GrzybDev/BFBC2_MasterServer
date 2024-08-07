from datetime import datetime

from pydantic import BaseModel, Field


class Attachment(BaseModel):
    key: str
    type: str
    data: str


class Target(BaseModel):
    name: str
    id: int
    type: int


class MessageResponse(BaseModel):
    attachments: list[Attachment]
    deliveryType: str
    messageId: int
    messageType: str
    purgeStrategy: str
    from_: Target = Field(validation_alias="from")
    to: list[Target]
    timeSent: datetime
    expiration: datetime
