from typing import Optional

from bfbc2_masterserver.messages.plasma.account.NuGetAccount import NuGetAccountResponse
from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.plasma.Entitlement import Entitlement


class NuGetAccountByNuidRequest(PlasmaTransaction):
    nuid: str


class NuGetAccountByNuidResponse(NuGetAccountResponse):
    pass
