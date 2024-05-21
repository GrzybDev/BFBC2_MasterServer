from typing import Optional

from pydantic import BaseModel

from bfbc2_masterserver.enumerators.ErrorCode import ErrorCode
from bfbc2_masterserver.messages.plasma.PlasmaTransaction import PlasmaTransaction


class Error(BaseModel):
    fieldName: str
    fieldError: int
    value: Optional[str] = None


class PlasmaError(PlasmaTransaction):
    errorCode: ErrorCode
    localizedMessage: str
    errorContainer: list[Error]
    TID: Optional[int] = None
