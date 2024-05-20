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
