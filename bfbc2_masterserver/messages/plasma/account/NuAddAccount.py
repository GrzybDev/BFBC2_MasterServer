from datetime import datetime

from pydantic import EmailStr, SecretStr, field_validator, model_validator

from bfbc2_masterserver.messages.plasma.PlasmaTransaction import PlasmaTransaction
from bfbc2_masterserver.tools.country_list import COUNTRY_LIST


class NuAddAccountRequest(PlasmaTransaction):
    nuid: EmailStr
    password: SecretStr
    globalOptin: bool
    thirdPartyOptin: bool
    parentalEmail: str
    DOBDay: int
    DOBMonth: int
    DOBYear: int
    zipCode: str
    country: str
    language: str
    tosVersion: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")

        return v

    @model_validator(mode="after")
    def validate_dob(self):
        dateToday = datetime.now()
        age = (
            dateToday.year
            - self.DOBYear
            - ((dateToday.month, dateToday.day) < (self.DOBMonth, self.DOBDay))
        )

        country_list = COUNTRY_LIST

        if self.country not in country_list:
            raise ValueError("Invalid country code")

        if country_list[self.country].get("registrationAgeLimit", 13) > age:
            raise ValueError("You are not old enough to register an account")

        return self


class NuAddAccountResponse(PlasmaTransaction):
    pass
