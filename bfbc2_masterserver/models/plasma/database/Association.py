from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, Relationship, SQLModel

from bfbc2_masterserver.enumerators.plasma.AssocationType import AssocationType

if TYPE_CHECKING:
    from bfbc2_masterserver.models.plasma.database.Persona import Persona


class Association(SQLModel, table=True):
    # Association is a link between two personas.

    id: int = Field(default=None, primary_key=True)
    owner: "Persona" = Relationship(
        back_populates="associations",
        sa_relationship_kwargs=dict(foreign_keys="[Association.owner_id]"),
    )
    owner_id: int = Field(default=None, foreign_key="persona.id")
    target: "Persona" = Relationship(
        back_populates="associations",
        sa_relationship_kwargs=dict(foreign_keys="[Association.target_id]"),
    )
    target_id: int = Field(default=None, foreign_key="persona.id")
    type: AssocationType

    createdAt: datetime = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now()),
    )

    updatedAt: datetime = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True), onupdate=func.now(), server_default=func.now()
        ),
    )
