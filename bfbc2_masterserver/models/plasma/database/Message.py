from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, Relationship, SQLModel

from bfbc2_masterserver.models.plasma.database.MessageAttachment import (
    MessageAttachment,
)

if TYPE_CHECKING:
    from bfbc2_masterserver.models.plasma.database.Persona import Persona


class Message(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)

    sender: "Persona" = Relationship(
        back_populates="messagesSent",
        sa_relationship_kwargs=dict(
            foreign_keys="[Message.sender_id]", lazy="selectin"
        ),
    )
    sender_id: int | None = Field(default=None, foreign_key="persona.id")

    recipient: "Persona" = Relationship(
        back_populates="messages",
        sa_relationship_kwargs=dict(
            foreign_keys="[Message.recipient_id]", lazy="selectin"
        ),
    )
    recipient_id: int | None = Field(default=None, foreign_key="persona.id")

    attachments: list["MessageAttachment"] = Relationship(
        back_populates="message",
        sa_relationship_kwargs=dict(lazy="selectin"),
        cascade_delete=True,
    )

    deliveryType: str
    messageType: str
    purgeStrategy: str

    timeSent: datetime = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now()),
    )

    expiration: datetime = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True)),
    )
