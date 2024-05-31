from enum import Enum

from bfbc2_masterserver.services.plasma.account import AccountService


class PlasmaService(Enum):
    ConnectService = "fsys"
    AccountService = "acct"
    AssociationService = "asso"
    MessageService = "xmsg"
    PresenceService = "pres"
