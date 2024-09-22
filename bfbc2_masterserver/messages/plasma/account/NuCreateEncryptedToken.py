from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.plasma.Attribute import Attribute


class NuCreateEncryptedTokenRequest(PlasmaTransaction):
    expires: int
    attributes: list[Attribute]


class NuCreateEncryptedTokenResponse(PlasmaTransaction):
    # Couldn't find any response for this transaction in my poor RE effort
    pass
