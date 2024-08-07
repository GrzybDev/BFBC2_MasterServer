from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from bfbc2_masterserver.models.plasma.database.Message import Message


class MessageAttachment(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)

    message: "Message" = Relationship(back_populates="attachments")
    message_id: int = Field(default=None, foreign_key="message.id")

    key: str
    type: str
    data: str
