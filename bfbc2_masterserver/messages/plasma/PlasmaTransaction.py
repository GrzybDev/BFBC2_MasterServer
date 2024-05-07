from typing import Optional

from pydantic import BaseModel

from bfbc2_masterserver.enumerators.Transaction import Transaction


class PlasmaTransaction(BaseModel):
    """
    The PlasmaTransaction class is a subclass of the BaseModel class from the Pydantic library.

    This class represents a transaction in the Plasma system. It has a single attribute, TXN, which represents the transaction type and is optional.

    Attributes:
        TXN (Optional[Transaction]): The type of the transaction. This attribute is optional and defaults to None.

    Methods:
        The PlasmaTransaction class inherits methods from the BaseModel class.
    """

    TXN: Optional[Transaction] = None
