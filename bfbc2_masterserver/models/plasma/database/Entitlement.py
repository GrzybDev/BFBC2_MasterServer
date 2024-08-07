from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from bfbc2_masterserver.models.plasma.database.Account import Account


class Entitlement(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    owner: "Account" = Relationship(
        back_populates="entitlements", sa_relationship_kwargs=dict(lazy="selectin")
    )
    owner_id: int | None = Field(default=None, foreign_key="account.id")

    tag: str | None = None
    grantDate: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now()),
    )
    terminationDate: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime(timezone=True), nullable=True)
    )

    groupName: Optional[str] = None
    productId: Optional[str] = None
    version: int = 0

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
