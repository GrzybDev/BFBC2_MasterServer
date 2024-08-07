from enum import Enum


class FESLTransaction(Enum):
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
    NuEntitleUser = "NuEntitleUser"
    NuLookupUserInfo = "NuLookupUserInfo"
    NuGrantEntitlement = "NuGrantEntitlement"

    # Plasma (Assocation)
    GetAssociations = "GetAssociations"
    AddAssociations = "AddAssociations"

    # Plasma (Extensible Message)
    ModifySettings = "ModifySettings"
    GetMessages = "GetMessages"

    # Plasma (PlayNow)
    Start = "Start"
    Status = "Status"

    # Plasma (Presence)
    SetPresenceStatus = "SetPresenceStatus"

    # Plasma (Ranking)
    GetStats = "GetStats"
    GetRankedStatsForOwners = "GetRankedStatsForOwners"
    GetRankedStats = "GetRankedStats"
    GetTopNAndStats = "GetTopNAndStats"

    # Plasma (Record)
    GetRecordAsMap = "GetRecordAsMap"
    GetRecord = "GetRecord"
