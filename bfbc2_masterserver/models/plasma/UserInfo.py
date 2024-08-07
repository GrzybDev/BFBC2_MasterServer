from pydantic import BaseModel


class UserInfoRequest(BaseModel):
    userName: str


class UserInfo(BaseModel):
    userName: str
    namespace: str
    userId: int
    masterUserId: int
