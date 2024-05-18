from pydantic import BaseModel


class PingSite(BaseModel):
    """
    Represents a ping site.

    Attributes:
        name (str): The name of the ping site.
        type (int): The type of the ping site.
        addr (str): The address of the ping site.
    """

    name: str
    type: int
    addr: str
