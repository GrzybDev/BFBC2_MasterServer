from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, Relationship, SQLModel

from bfbc2_masterserver.enumerators.plasma.RecordName import RecordName

if TYPE_CHECKING:
    from bfbc2_masterserver.models.plasma.database.Persona import Persona


class Record(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)

    owner: "Persona" = Relationship(back_populates="records")
    owner_id: int | None = Field(default=None, foreign_key="persona.id")

    key: str
    value: str
    type: RecordName

    updatedAt: datetime = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True), onupdate=func.now(), server_default=func.now()
        ),
    )
