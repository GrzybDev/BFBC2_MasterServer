from bfbc2_masterserver.messages.plasma.PlasmaTransaction import PlasmaTransaction


class GetTelemetryTokenRequest(PlasmaTransaction):
    pass


class GetTelemetryTokenResponse(PlasmaTransaction):
    telemetryToken: str
    enabled: str
    filters: str
    disabled: str
