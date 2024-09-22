from enum import Enum


class FESLTransaction(Enum):
    # Universal
    TransactionException = "TransactionException"

    # Plasma (Connect)
    Hello = "Hello"
    MemCheck = "MemCheck"
    GetPingSites = "GetPingSites"
    Ping = "Ping"
    Goodbye = "Goodbye"
    # Never called during my tests, but implemented in game code
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
    NuSearchOwners = "NuSearchOwners"
    # Never called during my tests, but implemented in game code
    NuCreateEncryptedToken = "NuCreateEncryptedToken"
    NuSuggestPersonas = "NuSuggestPersonas"
    NuUpdatePassword = "NuUpdatePassword"
    NuGetAccount = "NuGetAccount"
    NuGetAccountByNuid = "NuGetAccountByNuid"
    NuGetAccountByPS3Ticket = "NuGetAccountByPS3Ticket"  # PS3 Only?
    NuUpdateAccount = "NuUpdateAccount"
    GameSpyPreAuth = "GameSpyPreAuth"  # GameSpy leftover?
    NuXBL360Login = "NuXBL360Login"  # Xbox 360 Only?
    NuXBL360AddAccount = "NuXBL360AddAccount"  # Xbox 360 Only?
    NuPS3Login = "NuPS3Login"  # PS3 Only?
    NuPS3AddAccount = "NuPS3AddAccount"  # PS3 Only?
    NuGetEntitlementCount = "NuGetEntitlementCount"

    # Plasma (Assocation)
    GetAssociations = "GetAssociations"
    AddAssociations = "AddAssociations"
    NotifyAssociationUpdate = "NotifyAssociationUpdate"
    DeleteAssociations = "DeleteAssociations"
    GetAssociationsCount = "GetAssociationsCount"

    # Plasma (Extensible Message)
    ModifySettings = "ModifySettings"
    GetMessages = "GetMessages"
    SendMessage = "SendMessage"
    AsyncMessageEvent = "AsyncMessageEvent"
    GetMessageAttachments = "GetMessageAttachments"
    DeleteMessages = "DeleteMessages"
    PurgeMessages = "PurgeMessages"
    AsyncPurgedEvent = "AsyncPurgedEvent"

    # Plasma (PlayNow)
    Start = "Start"
    Status = "Status"

    # Plasma (Presence)
    SetPresenceStatus = "SetPresenceStatus"
    PresenceSubscribe = "PresenceSubscribe"
    PresenceUnsubscribe = "PresenceUnsubscribe"
    AsyncPresenceStatusEvent = "AsyncPresenceStatusEvent"

    # Plasma (Ranking)
    GetStats = "GetStats"
    GetRankedStatsForOwners = "GetRankedStatsForOwners"
    GetRankedStats = "GetRankedStats"
    GetTopNAndStats = "GetTopNAndStats"
    UpdateStats = "UpdateStats"
    # Never called during my tests, but implemented in game code
    GetStatsForOwners = "GetStatsForOwners"
    GetTopN = "GetTopN"
    GetTopNAndMe = "GetTopNAndMe"
    GetDateRange = "GetDateRange"

    # Plasma (Record)
    GetRecordAsMap = "GetRecordAsMap"
    GetRecord = "GetRecord"
    AddRecord = "AddRecord"
    UpdateRecord = "UpdateRecord"
    AddRecordAsMap = "AddRecordAsMap"
    UpdateRecordAsMap = "UpdateRecordAsMap"
