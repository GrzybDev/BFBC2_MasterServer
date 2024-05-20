from pydantic import field_validator

from bfbc2_masterserver.messages.plasma.PlasmaTransaction import PlasmaTransaction


class NuAddPersonaRequest(PlasmaTransaction):
    name: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str):
        if len(v) <= 4 and len(v) >= 16:
            raise ValueError("Persona name must be between 4 and 16 characters long")

        # A-Z, a-z, 0-9
        if not v.isalnum():
            raise ValueError("Persona name must only contain alphanumeric characters")

        return v


class NuAddPersonaResponse(PlasmaTransaction):
    pass
