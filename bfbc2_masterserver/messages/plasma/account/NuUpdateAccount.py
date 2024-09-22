from typing import Optional

from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction


class NuUpdateAccountRequest(PlasmaTransaction):
    nuid: str
    password: str
    globalOptin: str
    thirdPartyOptin: str

    parentalEmail: Optional[str]
    DOBDay: Optional[int]
    DOBMonth: Optional[int]
    DOBYear: Optional[int]
    first_Name: Optional[str]
    last_Name: Optional[str]
    gender: Optional[str]
    street: Optional[str]
    street2: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zipCode: Optional[str]
    country: Optional[str]
    language: Optional[str]


class NuUpdateAccountResponse(PlasmaTransaction):
    pass
