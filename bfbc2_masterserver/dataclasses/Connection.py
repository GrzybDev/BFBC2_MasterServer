from dataclasses import dataclass
from typing import Optional

from bfbc2_masterserver.enumerators.client.ClientLocale import ClientLocale
from bfbc2_masterserver.enumerators.client.ClientPlatform import ClientPlatform
from bfbc2_masterserver.enumerators.client.ClientType import ClientType
from bfbc2_masterserver.models.plasma.database.Account import Account
from bfbc2_masterserver.models.plasma.database.Persona import Persona
from bfbc2_masterserver.models.theater.database.Game import Game


@dataclass
class BaseConnection:
    clientName: Optional[str] = None
    clientVersion: Optional[str] = None
    locale: Optional[ClientLocale] = None
    platform: Optional[ClientPlatform] = None
    type: Optional[ClientType] = None
    fragmentSize: Optional[int] = None

    internalIp: Optional[str] = None
    internalPort: Optional[int] = None

    account: Optional[Account] = None
    accountSession: Optional[str] = None
    persona: Optional[Persona] = None
    personaSession: Optional[str] = None

    game: Optional[Game] = None
