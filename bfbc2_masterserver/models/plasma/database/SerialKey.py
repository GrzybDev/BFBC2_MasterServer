from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, Relationship, SQLModel

from bfbc2_masterserver.models.plasma.database.SerialKeyLink import SerialKeyLink

if TYPE_CHECKING:
    from bfbc2_masterserver.models.plasma.database.SerialKeyTarget import (
        SerialKeyTarget,
    )


class SerialKey(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    key: str = Field(unique=True)
    reusable: bool = False
    used: bool = False
    used_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), onupdate=func.now(), nullable=True),
    )
    owner: int | None = Field(default=None, foreign_key="account.id")

    targets: list["SerialKeyTarget"] = Relationship(
        back_populates="keys", link_model=SerialKeyLink
    )
