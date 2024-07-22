from bfbc2_masterserver.models.general.PlasmaTransaction import PlasmaTransaction


class GetTelemetryTokenRequest(PlasmaTransaction):
    pass


class GetTelemetryTokenResponse(PlasmaTransaction):
    telemetryToken: str
    enabled: str
    filters: str
    disabled: str
