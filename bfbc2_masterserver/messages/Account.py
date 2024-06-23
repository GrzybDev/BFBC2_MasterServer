from typing import Optional

from pydantic import BaseModel, SecretStr


class Account(BaseModel):
    id: int
    nuid: str
    password: SecretStr
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
    serviceAccount: bool = False
