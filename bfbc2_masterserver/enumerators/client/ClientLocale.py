from enum import Enum


class ClientLocale(Enum):
    """
    The ClientLocale class is a subclass of the Enum class from the enum module.

    This class represents various client locales that can be used in the system. Each locale is represented by a unique string value.

    Attributes:
        English (str): The string value for English locale.
        French (str): The string value for French locale.
        German (str): The string value for German locale.
        Spanish (str): The string value for Spanish locale.
        Italian (str): The string value for Italian locale.
        Japanese (str): The string value for Japanese locale.
        Russian (str): The string value for Russian locale.
        Polish (str): The string value for Polish locale.
    """

    English = "en_US"
    French = "fr_FR"
    German = "de"
    Spanish = "es"
    Italian = "it"
    Japanese = "ja"
    Russian = "ru"
    Polish = "pl"
