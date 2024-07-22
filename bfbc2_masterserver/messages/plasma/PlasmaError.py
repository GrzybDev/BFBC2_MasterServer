from typing import Optional

from bfbc2_masterserver.enumerators.ErrorCode import ErrorCode
from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.plasma.message.Error import Error


class PlasmaError(PlasmaTransaction):
    errorCode: ErrorCode
    localizedMessage: str
    errorContainer: list[Error]
    TID: Optional[int] = None
