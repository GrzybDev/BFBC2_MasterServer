from typing import Optional

from pydantic import BaseModel


class Country(BaseModel):
    """
    Represents a country.

    Attributes:
        ISOCode (str): The ISO code of the country.
        description (str): The description of the country.

        allowEmailsDefaultValue (Optional[int]): The default value for allowing emails.
        parentalControlAgeLimit (Optional[int]): The parental control age limit.
        registrationAgeLimit (Optional[int]): The registration age limit.
    """

    ISOCode: str
    description: str

    allowEmailsDefaultValue: Optional[int] = None
    parentalControlAgeLimit: Optional[int] = None
    registrationAgeLimit: Optional[int] = None
