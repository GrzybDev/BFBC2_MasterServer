from typing import TYPE_CHECKING

from pyexpat.errors import messages
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from bfbc2_masterserver.models.plasma.database.Account import Account
    from bfbc2_masterserver.models.plasma.database.Association import Association
    from bfbc2_masterserver.models.plasma.database.Message import Message
    from bfbc2_masterserver.models.plasma.database.Ranking import Ranking
    from bfbc2_masterserver.models.plasma.database.Record import Record
    from bfbc2_masterserver.models.theater.database.Game import Game


class Persona(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    owner: "Account" = Relationship(
        back_populates="personas", sa_relationship_kwargs=dict(lazy="selectin")
    )
    owner_id: int | None = Field(default=None, foreign_key="account.id")
    name: str = Field(unique=True)

    associations: list["Association"] = Relationship(
        back_populates="owner",
        sa_relationship_kwargs=dict(foreign_keys="[Association.owner_id]"),
    )

    stats: "Ranking" = Relationship(back_populates="owner")
    records: "Record" = Relationship(back_populates="owner")

    messages: list["Message"] = Relationship(
        back_populates="recipient",
        sa_relationship_kwargs=dict(foreign_keys="[Message.recipient_id]"),
    )

    messagesSent: list["Message"] = Relationship(
        back_populates="sender",
        sa_relationship_kwargs=dict(foreign_keys="[Message.sender_id]"),
    )

    games: list["Game"] = Relationship(back_populates="owner")
