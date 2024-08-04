from enum import Enum


class FESLService(Enum):
    ConnectService = "fsys"
    AccountService = "acct"
    AssociationService = "asso"
    MessageService = "xmsg"
    PlayNowService = "pnow"
    PresenceService = "pres"
    RankingService = "rank"
    RecordService = "recp"
