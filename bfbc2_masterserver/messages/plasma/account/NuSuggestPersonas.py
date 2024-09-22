from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.plasma.UserInfo import UserInfo, UserInfoRequest


class NuSuggestPersonasRequest(PlasmaTransaction):
    name: str
    maxSuggestions: int
    keywords: list[str]


class NuSuggestPersonasResponse(PlasmaTransaction):
    names: list[str]
