from typing import Optional

from pydantic import BaseModel


class MemCheck(BaseModel):
    """
    Never saw MemCheck containing any data, original server also always sends empty MemCheck.

    But those are the fields that game expects to be present in the MemCheck message if it's not empty.

    Never seen that in the wild, and above is just a guess based on my client reverse engineering.
    No idea how this affects the client (if at all), but original server never sends it either so it's probably leftover.

    Attributes:
        addr (Optional[int]): The address of the memory check.
        len (Optional[int]): The length of the memory check.
    """

    addr: Optional[int] = None
    len: Optional[int] = None
