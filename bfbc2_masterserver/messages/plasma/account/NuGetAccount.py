from typing import Optional

from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.plasma.Entitlement import Entitlement


class NuGetAccountRequest(PlasmaTransaction):
    nuid: Optional[str]


class NuGetAccountResponse(PlasmaTransaction):
    nuid: str
    parentalEmail: Optional[str]
    firstName: Optional[str]
    lastName: Optional[str]
    street: Optional[str]
    street2: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip: Optional[str]
    country: Optional[str]
    language: Optional[str]
    userId: int
    dOBMonth: Optional[int]
    dOBDay: Optional[int]
    dOBYear: Optional[int]
    globalCommOptin: Optional[str]
    thirdPartyMailFlag: Optional[str]
