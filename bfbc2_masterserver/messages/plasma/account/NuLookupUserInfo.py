from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.models.plasma.UserInfo import UserInfo, UserInfoRequest


class NuLookupUserInfoRequest(PlasmaTransaction):
    userInfo: list[UserInfoRequest]


class NuLookupUserInfoResponse(PlasmaTransaction):
    userInfo: list[UserInfo]
