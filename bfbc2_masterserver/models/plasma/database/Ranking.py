from decimal import Decimal
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from bfbc2_masterserver.models.plasma.database.Persona import Persona


class Ranking(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)

    owner: "Persona" = Relationship(back_populates="stats")
    owner_id: int | None = Field(default=None, foreign_key="persona.id")

    key: str
    value: Decimal = Field(default=0, decimal_places=3)
