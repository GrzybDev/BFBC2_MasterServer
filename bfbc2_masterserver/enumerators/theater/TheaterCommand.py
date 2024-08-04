from enum import Enum


class TheaterCommand(Enum):
    Connect = "CONN"
    Login = "USER"
    Echo = "ECHO"
    GetGameDetails = "GDAT"
    GetLobbyList = "LLST"
    LobbyData = "LDAT"
    GetGameList = "GLST"
    GameData = "GDAT"
    CreateGame = "CGAM"
    UpdateBracket = "UBRA"
    UpdateGame = "UGAM"
    UpdateGameDetails = "UGDE"
    EnterGameRequest = "EGAM"
    EnterGameHostRequest = "EGRQ"
    EnterGameNotice = "EGEG"
    EnterGameHostResponse = "EGRS"
    LeaveGame = "ECNL"
    PlayerExited = "PLVT"
    PlayerEntered = "PENT"
