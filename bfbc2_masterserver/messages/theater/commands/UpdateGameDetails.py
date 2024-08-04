from typing import Optional

from pydantic import Field, model_validator

from bfbc2_masterserver.models.general.TheaterTransaction import TheaterTransaction


class UpdateGameDetailsRequest(TheaterTransaction):
    class Config:
        extra = "forbid"

    LID: int
    GID: int

    gameAutoBalance: bool = Field(alias="D-AutoBalance", default=None)
    gameCrosshair: bool = Field(alias="D-Crosshair", default=None)
    gameFriendlyFire: float = Field(alias="D-FriendlyFire", default=None)
    gameKillCam: bool = Field(alias="D-KillCam", default=None)
    gameMiniMap: bool = Field(alias="D-Minimap", default=None)
    gameMiniMapSpotting: bool = Field(alias="D-MinimapSpotting", default=None)
    gameThirdPersonVehicleCameras: bool = Field(
        alias="D-ThirdPersonVehicleCameras", default=None
    )
    gameThreeDSpotting: bool = Field(alias="D-ThreeDSpotting", default=None)

    playerData: Optional[list[str]] = None
    serverDescriptions: Optional[list[str]] = None

    @model_validator(mode="before")
    def aggregate_pdats(cls, values):
        # Collect all D_pdatXY fields into D_pdats
        d_pdats = []

        for i in range(0, 99):
            d_pdat = values.get(f"D-pdat{str(i).zfill(2)}")
            if d_pdat is not None:
                d_pdats.append(d_pdat)
                del values[f"D-pdat{str(object=i).zfill(2)}"]

        values["playerData"] = d_pdats
        return values

    @model_validator(mode="before")
    def aggregate_descriptions(cls, values):
        # TODO
        del values["D-ServerDescriptionCount"]
        return values


class UpdateGameDetailsResponse(TheaterTransaction):
    pass
