from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, Relationship, SQLModel

from bfbc2_masterserver.models.plasma.database.SerialKeyLink import SerialKeyLink

if TYPE_CHECKING:
    from bfbc2_masterserver.models.plasma.database.SerialKey import SerialKey


class SerialKeyTarget(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)

    keys: list["SerialKey"] = Relationship(
        back_populates="targets", link_model=SerialKeyLink
    )

    tag: str
    start_date: datetime = Field(
        default=None, sa_column=Column(DateTime(timezone=True), nullable=True)
    )
    duration: Optional[int] = None

    groupName: Optional[str] = None
    productId: Optional[str] = None
    version: int = 0
