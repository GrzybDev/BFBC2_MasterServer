from typing import TYPE_CHECKING, Optional

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from bfbc2_masterserver.models.plasma.database.Entitlement import Entitlement
    from bfbc2_masterserver.models.plasma.database.Persona import Persona


class Account(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    nuid: EmailStr = Field(unique=True)
    password: str
    serviceAccount: bool = False
    globalOptin: bool = False
    thirdPartyOptin: bool = False
    parentalEmail: Optional[str] = None
    DOBDay: Optional[int] = None
    DOBMonth: Optional[int] = None
    DOBYear: Optional[int] = None
    zipCode: Optional[str] = None
    country: Optional[str] = None
    language: Optional[str] = None
    tosVersion: Optional[str] = None

    personas: list["Persona"] = Relationship(
        back_populates="owner", cascade_delete=True
    )
    entitlements: list["Entitlement"] = Relationship(
        back_populates="owner", cascade_delete=True
    )
