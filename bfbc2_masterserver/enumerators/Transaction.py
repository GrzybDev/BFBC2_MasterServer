from enum import Enum


class Transaction(Enum):
    # Plasma (Connect)
    Hello = "Hello"
    MemCheck = "MemCheck"
    GetPingSites = "GetPingSites"
    Ping = "Ping"
    Goodbye = "Goodbye"
    Suicide = "Suicide"

    # Plasma (Account)
    GetCountryList = "GetCountryList"
    NuGetTos = "NuGetTos"
    NuAddAccount = "NuAddAccount"
    NuLogin = "NuLogin"
    NuGetPersonas = "NuGetPersonas"
    NuAddPersona = "NuAddPersona"
    NuDisablePersona = "NuDisablePersona"
    NuLoginPersona = "NuLoginPersona"
    NuEntitleGame = "NuEntitleGame"
    GetTelemetryToken = "GetTelemetryToken"
    NuGetEntitlements = "NuGetEntitlements"
    GetLockerURL = "GetLockerURL"

    # Plasma (Assocation)
    GetAssociations = "GetAssociations"

    # Plasma (Extensible Message)
    ModifySettings = "ModifySettings"
    GetMessages = "GetMessages"

    # Plasma (Presence)
    SetPresenceStatus = "SetPresenceStatus"

    # Plasma (Ranking)
    GetStats = "GetStats"

    # Plasma (Record)
    GetRecordAsMap = "GetRecordAsMap"
    GetRecord = "GetRecord"
